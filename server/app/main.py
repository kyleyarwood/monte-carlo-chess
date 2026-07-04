"""FastAPI app: room creation over REST, gameplay over WebSockets."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import protocol
from .engine import IllegalMoveError, Move, apply_move
from .rooms import RoomManager

app = FastAPI(title="Monte Carlo Chess")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = RoomManager()


@app.post("/api/games")
async def create_game() -> dict:
    room = manager.create()
    return {"code": room.code}


@app.websocket("/ws/{code}")
async def game_socket(websocket: WebSocket, code: str) -> None:
    room = manager.get(code)
    if room is None:
        await websocket.accept()
        await websocket.send_json(protocol.error("Game not found."))
        await websocket.close()
        return

    async with room.lock:
        seat = room.free_seat()
        if seat is None:
            await websocket.accept()
            await websocket.send_json(protocol.error("Game is full."))
            await websocket.close()
            return
        await websocket.accept()
        room.players[seat] = websocket

    await websocket.send_json(protocol.joined(seat, room.code))
    await websocket.send_json(protocol.state(room.state))
    await room.broadcast(protocol.players(room))

    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") != "move":
                await websocket.send_json(protocol.error("Unknown message type."))
                continue
            async with room.lock:
                if not room.is_full:
                    await websocket.send_json(
                        protocol.error("Waiting for an opponent to join.")
                    )
                    continue
                if room.state.turn is not seat or room.state.is_over:
                    await websocket.send_json(protocol.error("It is not your turn."))
                    continue
                try:
                    move = Move.from_dict(data["move"])
                    result = apply_move(room.state, move, room.rng)
                except (IllegalMoveError, KeyError, TypeError, ValueError):
                    await websocket.send_json(protocol.error("Illegal move."))
                    continue
                await room.broadcast(protocol.move_result(result, room.state))
    except WebSocketDisconnect:
        pass
    finally:
        current_seat = room.seat_of(websocket)
        if current_seat is not None:
            room.players[current_seat] = None
        if room.is_empty:
            manager.remove(room.code)
        else:
            await room.broadcast(protocol.players(room))


# Serve the built client (client/dist) when it exists, for production use.
_client_dist = Path(__file__).resolve().parents[2] / "client" / "dist"
if _client_dist.is_dir():
    app.mount("/", StaticFiles(directory=_client_dist, html=True), name="client")

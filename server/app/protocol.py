"""Builders for the JSON messages the server sends over WebSockets.

Client -> server messages:
    {"type": "move", "move": {"from": [r, c], "to": [r, c], "promotion": str|null}}
"""

from __future__ import annotations

from .engine import Color, GameState, MoveResult, result_to_dict, state_to_dict
from .rooms import Room


def joined(color: Color, code: str) -> dict:
    return {"type": "joined", "color": color.value, "code": code}


def state(game_state: GameState) -> dict:
    return {"type": "state", "state": state_to_dict(game_state)}


def move_result(result: MoveResult, game_state: GameState) -> dict:
    return {
        "type": "move_result",
        "result": result_to_dict(result),
        "state": state_to_dict(game_state),
    }


def players(room: Room) -> dict:
    return {
        "type": "players",
        "players": {
            color.value: ws is not None for color, ws in room.players.items()
        },
    }


def error(message: str) -> dict:
    return {"type": "error", "message": message}

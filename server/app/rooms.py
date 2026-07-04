"""In-memory game rooms: one Room per shareable code."""

from __future__ import annotations

import asyncio
import random
import secrets
from dataclasses import dataclass, field
from typing import Optional

from fastapi import WebSocket

from .engine import Color, GameState

# Unambiguous uppercase alphabet (no O/0, I/1).
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
CODE_LENGTH = 6


@dataclass
class Room:
    code: str
    state: GameState = field(default_factory=GameState)
    rng: random.Random = field(default_factory=random.Random)
    players: dict[Color, Optional[WebSocket]] = field(
        default_factory=lambda: {Color.WHITE: None, Color.BLACK: None}
    )
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    def free_seat(self) -> Optional[Color]:
        for color in (Color.WHITE, Color.BLACK):
            if self.players[color] is None:
                return color
        return None

    def seat_of(self, socket: WebSocket) -> Optional[Color]:
        for color, ws in self.players.items():
            if ws is socket:
                return color
        return None

    @property
    def is_full(self) -> bool:
        return all(ws is not None for ws in self.players.values())

    @property
    def is_empty(self) -> bool:
        return all(ws is None for ws in self.players.values())

    async def broadcast(self, message: dict) -> None:
        for ws in self.players.values():
            if ws is not None:
                try:
                    await ws.send_json(message)
                except Exception:
                    pass  # a dropped socket is handled by its own reader loop


class RoomManager:
    def __init__(self) -> None:
        self.rooms: dict[str, Room] = {}

    def create(self) -> Room:
        while True:
            code = "".join(
                secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH)
            )
            if code not in self.rooms:
                break
        room = Room(code=code)
        self.rooms[code] = room
        return room

    def get(self, code: str) -> Optional[Room]:
        return self.rooms.get(code.upper())

    def remove(self, code: str) -> None:
        self.rooms.pop(code, None)

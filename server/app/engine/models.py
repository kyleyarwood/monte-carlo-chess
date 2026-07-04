"""Core data structures for Monte Carlo Chess.

Board coordinates are (row, col) with row 0 = rank 1 (white's home rank)
and col 0 = file a. White pawns move toward higher rows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Color(str, Enum):
    WHITE = "white"
    BLACK = "black"

    @property
    def opponent(self) -> "Color":
        return Color.BLACK if self is Color.WHITE else Color.WHITE


class Kind(str, Enum):
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


INITIAL_POWER = {
    Kind.PAWN: 1,
    Kind.KNIGHT: 3,
    Kind.BISHOP: 3,
    Kind.KING: 4,
    Kind.ROOK: 5,
    Kind.QUEEN: 9,
}

PROMOTION_KINDS = (Kind.KNIGHT, Kind.BISHOP, Kind.ROOK, Kind.QUEEN)

# Turns without a pawn move, castle, or battle before the game is
# resolved by chance.
TURN_LIMIT = 50

BOARD_SIZE = 8


@dataclass
class Piece:
    kind: Kind
    color: Color
    power: int
    has_moved: bool = False


@dataclass(frozen=True)
class Move:
    from_sq: tuple[int, int]
    to_sq: tuple[int, int]
    promotion: Optional[Kind] = None

    def to_dict(self) -> dict:
        return {
            "from": list(self.from_sq),
            "to": list(self.to_sq),
            "promotion": self.promotion.value if self.promotion else None,
        }

    @staticmethod
    def from_dict(data: dict) -> "Move":
        promotion = Kind(data["promotion"]) if data.get("promotion") else None
        return Move(tuple(data["from"]), tuple(data["to"]), promotion)


BACK_RANK_ORDER = (
    Kind.ROOK,
    Kind.KNIGHT,
    Kind.BISHOP,
    Kind.QUEEN,
    Kind.KING,
    Kind.BISHOP,
    Kind.KNIGHT,
    Kind.ROOK,
)


def initial_board() -> list[list[Optional[Piece]]]:
    board: list[list[Optional[Piece]]] = [
        [None] * BOARD_SIZE for _ in range(BOARD_SIZE)
    ]
    for col, kind in enumerate(BACK_RANK_ORDER):
        board[0][col] = Piece(kind, Color.WHITE, INITIAL_POWER[kind])
        board[7][col] = Piece(kind, Color.BLACK, INITIAL_POWER[kind])
    for col in range(BOARD_SIZE):
        board[1][col] = Piece(Kind.PAWN, Color.WHITE, INITIAL_POWER[Kind.PAWN])
        board[6][col] = Piece(Kind.PAWN, Color.BLACK, INITIAL_POWER[Kind.PAWN])
    return board


@dataclass
class GameState:
    board: list[list[Optional[Piece]]] = field(default_factory=initial_board)
    turn: Color = Color.WHITE
    # Square a pawn skipped over on its last double push, capturable en passant.
    en_passant_target: Optional[tuple[int, int]] = None
    # Turns since the last pawn move, castle, or battle.
    quiet_turns: int = 0
    winner: Optional[Color] = None
    end_reason: Optional[str] = None

    @property
    def is_over(self) -> bool:
        return self.winner is not None

    def piece_at(self, sq: tuple[int, int]) -> Optional[Piece]:
        return self.board[sq[0]][sq[1]]

    def pieces(self, color: Color) -> list[Piece]:
        return [
            p for row in self.board for p in row if p is not None and p.color == color
        ]

    def total_power(self, color: Color) -> int:
        return sum(p.power for p in self.pieces(color))

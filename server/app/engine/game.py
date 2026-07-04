"""Game progression for Monte Carlo Chess: battles, leveling, endings.

All randomness flows through the `random.Random` instance passed to
`apply_move`, so tests can seed or stub outcomes.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

from .models import Color, GameState, Kind, Move, TURN_LIMIT
from .moves import is_castle, is_en_passant, legal_moves


@dataclass
class BattleReport:
    attacker_kind: Kind
    attacker_color: Color
    attacker_power: int
    defender_kind: Kind
    defender_power: int
    win_probability: float
    attacker_won: bool
    winner_power_after: int


@dataclass
class MoveResult:
    move: Move
    battle: Optional[BattleReport] = None
    castled: bool = False
    promoted_to: Optional[Kind] = None
    ended_by_chance: bool = False
    chance_white_probability: Optional[float] = None
    events: list[str] = field(default_factory=list)


class IllegalMoveError(Exception):
    pass


def apply_move(state: GameState, move: Move, rng: random.Random) -> MoveResult:
    """Apply `move` for the player to move, mutating `state`."""
    if state.is_over:
        raise IllegalMoveError("The game is already over.")
    if move not in legal_moves(state, state.turn):
        raise IllegalMoveError("Not a legal move.")

    piece = state.piece_at(move.from_sq)
    result = MoveResult(move=move)
    en_passant = is_en_passant(state, move)
    castled = is_castle(state, move)

    if en_passant:
        defender_sq = (move.from_sq[0], move.to_sq[1])
    else:
        defender_sq = move.to_sq
    defender = state.piece_at(defender_sq)

    resets_clock = castled or piece.kind is Kind.PAWN or defender is not None

    if defender is not None:
        result.battle = _resolve_battle(state, move, defender_sq, rng)
    else:
        _move_piece(state, move)
        if castled:
            _move_castle_rook(state, move)
            result.castled = True

    if state.piece_at(move.to_sq) is piece and move.promotion is not None:
        # Promotion changes movement but never the pawn's power level.
        piece.kind = move.promotion
        result.promoted_to = move.promotion

    state.en_passant_target = None
    if (
        piece.kind is Kind.PAWN
        and state.piece_at(move.to_sq) is piece
        and abs(move.to_sq[0] - move.from_sq[0]) == 2
    ):
        state.en_passant_target = (
            (move.from_sq[0] + move.to_sq[0]) // 2,
            move.from_sq[1],
        )

    state.quiet_turns = 0 if resets_clock else state.quiet_turns + 1

    _settle_outcome(state, result, rng)
    return result


def _resolve_battle(
    state: GameState, move: Move, defender_sq: tuple[int, int], rng: random.Random
) -> BattleReport:
    attacker = state.piece_at(move.from_sq)
    defender = state.piece_at(defender_sq)
    win_probability = attacker.power / (attacker.power + defender.power)
    attacker_won = rng.random() < win_probability

    report = BattleReport(
        attacker_kind=attacker.kind,
        attacker_color=attacker.color,
        attacker_power=attacker.power,
        defender_kind=defender.kind,
        defender_power=defender.power,
        win_probability=win_probability,
        attacker_won=attacker_won,
        winner_power_after=(
            attacker.power + defender.power  # winner absorbs the loser either way
        ),
    )

    if attacker_won:
        attacker.power += defender.power
        state.board[defender_sq[0]][defender_sq[1]] = None
        _move_piece(state, move)
    else:
        defender.power += attacker.power
        state.board[move.from_sq[0]][move.from_sq[1]] = None
    return report


def _move_piece(state: GameState, move: Move) -> None:
    piece = state.piece_at(move.from_sq)
    state.board[move.from_sq[0]][move.from_sq[1]] = None
    state.board[move.to_sq[0]][move.to_sq[1]] = piece
    piece.has_moved = True


def _move_castle_rook(state: GameState, move: Move) -> None:
    row = move.from_sq[0]
    rook_from, rook_to = (7, 5) if move.to_sq[1] == 6 else (0, 3)
    rook = state.board[row][rook_from]
    state.board[row][rook_from] = None
    state.board[row][rook_to] = rook
    rook.has_moved = True


def _settle_outcome(state: GameState, result: MoveResult, rng: random.Random) -> None:
    mover = state.turn
    opponent = mover.opponent

    if not state.pieces(opponent):
        state.winner = mover
        state.end_reason = "army_captured"
        return
    if not state.pieces(mover):
        # The mover's last piece just died in a failed attack.
        state.winner = opponent
        state.end_reason = "army_captured"
        return

    state.turn = opponent
    if state.quiet_turns >= TURN_LIMIT:
        _resolve_by_chance(state, result, rng, "turn_limit")
    elif not legal_moves(state, opponent):
        _resolve_by_chance(state, result, rng, "stalemate")


def _resolve_by_chance(
    state: GameState, result: MoveResult, rng: random.Random, reason: str
) -> None:
    white = state.total_power(Color.WHITE)
    black = state.total_power(Color.BLACK)
    white_probability = white / (white + black)
    state.winner = (
        Color.WHITE if rng.random() < white_probability else Color.BLACK
    )
    state.end_reason = reason
    result.ended_by_chance = True
    result.chance_white_probability = white_probability

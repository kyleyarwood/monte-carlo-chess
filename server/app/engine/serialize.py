"""JSON-friendly views of engine objects for the wire protocol."""

from __future__ import annotations

from .game import MoveResult
from .models import GameState, TURN_LIMIT
from .moves import legal_moves


def state_to_dict(state: GameState) -> dict:
    board = [
        [
            {
                "kind": piece.kind.value,
                "color": piece.color.value,
                "power": piece.power,
            }
            if piece is not None
            else None
            for piece in row
        ]
        for row in state.board
    ]
    return {
        "board": board,
        "turn": state.turn.value,
        "quietTurns": state.quiet_turns,
        "turnLimit": TURN_LIMIT,
        "winner": state.winner.value if state.winner else None,
        "endReason": state.end_reason,
        "legalMoves": [] if state.is_over else [
            m.to_dict() for m in legal_moves(state, state.turn)
        ],
    }


def result_to_dict(result: MoveResult) -> dict:
    battle = None
    if result.battle is not None:
        b = result.battle
        battle = {
            "attackerKind": b.attacker_kind.value,
            "attackerColor": b.attacker_color.value,
            "attackerPower": b.attacker_power,
            "defenderKind": b.defender_kind.value,
            "defenderPower": b.defender_power,
            "winProbability": b.win_probability,
            "attackerWon": b.attacker_won,
            "winnerPowerAfter": b.winner_power_after,
        }
    return {
        "move": result.move.to_dict(),
        "battle": battle,
        "castled": result.castled,
        "promotedTo": result.promoted_to.value if result.promoted_to else None,
        "endedByChance": result.ended_by_chance,
        "chanceWhiteProbability": result.chance_white_probability,
    }

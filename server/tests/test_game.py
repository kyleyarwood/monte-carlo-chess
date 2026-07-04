import random

import pytest

from app.engine.game import IllegalMoveError, apply_move
from app.engine.models import Color, GameState, Kind, Move, Piece, TURN_LIMIT


class FixedRandom(random.Random):
    """Returns queued values from random(); falls back to real randomness."""

    def __init__(self, *values):
        super().__init__()
        self.values = list(values)

    def random(self):
        if self.values:
            return self.values.pop(0)
        return super().random()


def empty_state(turn=Color.WHITE) -> GameState:
    return GameState(board=[[None] * 8 for _ in range(8)], turn=turn)


def put(state, sq, kind, color, power, has_moved=True):
    piece = Piece(kind, color, power, has_moved=has_moved)
    state.board[sq[0]][sq[1]] = piece
    return piece


def test_quiet_move_just_moves():
    state = empty_state()
    put(state, (0, 0), Kind.ROOK, Color.WHITE, 5)
    put(state, (7, 7), Kind.KING, Color.BLACK, 4)
    result = apply_move(state, Move((0, 0), (0, 1)), random.Random(0))
    assert state.piece_at((0, 1)).kind is Kind.ROOK
    assert result.battle is None
    assert state.turn is Color.BLACK
    assert state.quiet_turns == 1


def test_illegal_move_rejected():
    state = GameState()
    with pytest.raises(IllegalMoveError):
        apply_move(state, Move((0, 0), (5, 5)), random.Random(0))


def test_won_battle_moves_and_absorbs_power():
    state = empty_state()
    attacker = put(state, (0, 0), Kind.KNIGHT, Color.WHITE, 3)
    put(state, (2, 1), Kind.ROOK, Color.BLACK, 5)
    put(state, (7, 7), Kind.KING, Color.BLACK, 4)
    # win probability = 3/8; roll below it -> attacker wins
    result = apply_move(state, Move((0, 0), (2, 1)), FixedRandom(0.1))
    assert result.battle.attacker_won
    assert result.battle.win_probability == pytest.approx(3 / 8)
    assert state.piece_at((2, 1)) is attacker
    assert attacker.power == 8
    assert state.quiet_turns == 0


def test_lost_battle_removes_attacker_and_levels_defender():
    state = empty_state()
    put(state, (0, 0), Kind.KNIGHT, Color.WHITE, 3)
    defender = put(state, (2, 1), Kind.ROOK, Color.BLACK, 5)
    put(state, (0, 7), Kind.KING, Color.WHITE, 4)
    result = apply_move(state, Move((0, 0), (2, 1)), FixedRandom(0.9))
    assert not result.battle.attacker_won
    assert state.piece_at((0, 0)) is None
    assert state.piece_at((2, 1)) is defender
    assert defender.power == 8


def test_win_by_capturing_last_piece():
    state = empty_state()
    put(state, (0, 0), Kind.QUEEN, Color.WHITE, 9)
    put(state, (0, 5), Kind.PAWN, Color.BLACK, 1)
    result = apply_move(state, Move((0, 0), (0, 5)), FixedRandom(0.1))
    assert state.winner is Color.WHITE
    assert state.end_reason == "army_captured"
    assert result.battle.attacker_won


def test_loss_when_last_piece_dies_attacking():
    state = empty_state()
    put(state, (0, 0), Kind.QUEEN, Color.WHITE, 1)
    put(state, (0, 5), Kind.QUEEN, Color.BLACK, 9)
    apply_move(state, Move((0, 0), (0, 5)), FixedRandom(0.99))
    assert state.winner is Color.BLACK
    assert state.end_reason == "army_captured"


def test_king_is_capturable_and_game_continues():
    state = empty_state()
    put(state, (0, 0), Kind.ROOK, Color.WHITE, 5)
    put(state, (0, 5), Kind.KING, Color.BLACK, 4)
    put(state, (7, 7), Kind.PAWN, Color.BLACK, 1)
    apply_move(state, Move((0, 0), (0, 5)), FixedRandom(0.1))
    assert state.winner is None
    assert state.turn is Color.BLACK


def test_en_passant_success_removes_passed_pawn():
    state = empty_state()
    attacker = put(state, (4, 4), Kind.PAWN, Color.WHITE, 1)
    put(state, (4, 5), Kind.PAWN, Color.BLACK, 1)
    put(state, (7, 7), Kind.KING, Color.BLACK, 4)
    state.en_passant_target = (5, 5)
    result = apply_move(state, Move((4, 4), (5, 5)), FixedRandom(0.1))
    assert result.battle.attacker_won
    assert state.piece_at((5, 5)) is attacker
    assert state.piece_at((4, 5)) is None
    assert attacker.power == 2


def test_en_passant_failure_keeps_defender_in_place():
    state = empty_state()
    put(state, (4, 4), Kind.PAWN, Color.WHITE, 1)
    defender = put(state, (4, 5), Kind.PAWN, Color.BLACK, 1)
    put(state, (0, 0), Kind.KING, Color.WHITE, 4)
    state.en_passant_target = (5, 5)
    result = apply_move(state, Move((4, 4), (5, 5)), FixedRandom(0.9))
    assert not result.battle.attacker_won
    assert state.piece_at((4, 4)) is None
    assert state.piece_at((4, 5)) is defender
    assert defender.power == 2


def test_double_push_sets_en_passant_target():
    state = GameState()
    apply_move(state, Move((1, 4), (3, 4)), random.Random(0))
    assert state.en_passant_target == (2, 4)
    apply_move(state, Move((6, 0), (5, 0)), random.Random(0))
    assert state.en_passant_target is None


def test_promotion_keeps_pawn_power():
    state = empty_state()
    pawn = put(state, (6, 0), Kind.PAWN, Color.WHITE, 3)
    put(state, (7, 7), Kind.KING, Color.BLACK, 4)
    result = apply_move(
        state, Move((6, 0), (7, 0), promotion=Kind.QUEEN), random.Random(0)
    )
    assert pawn.kind is Kind.QUEEN
    assert pawn.power == 3
    assert result.promoted_to is Kind.QUEEN


def test_failed_promotion_capture_does_not_promote():
    state = empty_state()
    put(state, (6, 0), Kind.PAWN, Color.WHITE, 1)
    defender = put(state, (7, 1), Kind.ROOK, Color.BLACK, 5)
    put(state, (0, 0), Kind.KING, Color.WHITE, 4)
    apply_move(state, Move((6, 0), (7, 1), promotion=Kind.QUEEN), FixedRandom(0.99))
    assert state.piece_at((6, 0)) is None
    assert defender.kind is Kind.ROOK
    assert defender.power == 6


def test_castling_moves_rook_and_resets_clock():
    state = empty_state()
    put(state, (0, 4), Kind.KING, Color.WHITE, 4, has_moved=False)
    put(state, (0, 7), Kind.ROOK, Color.WHITE, 5, has_moved=False)
    put(state, (7, 7), Kind.KING, Color.BLACK, 4)
    state.quiet_turns = 10
    result = apply_move(state, Move((0, 4), (0, 6)), random.Random(0))
    assert result.castled
    assert state.piece_at((0, 6)).kind is Kind.KING
    assert state.piece_at((0, 5)).kind is Kind.ROOK
    assert state.quiet_turns == 0


def test_turn_limit_triggers_chance_resolution():
    state = empty_state()
    put(state, (0, 0), Kind.ROOK, Color.WHITE, 6)  # W = 6
    put(state, (7, 7), Kind.ROOK, Color.BLACK, 2)  # B = 2 -> white wins at 6/8
    state.quiet_turns = TURN_LIMIT - 1
    result = apply_move(state, Move((0, 0), (0, 1)), FixedRandom(0.5, 0.7))
    assert result.ended_by_chance
    assert result.chance_white_probability == pytest.approx(0.75)
    assert state.winner is Color.WHITE
    assert state.end_reason == "turn_limit"


def test_stalemate_triggers_chance_resolution():
    # Black's only piece is a pawn with no moves: blocked straight ahead
    # and nothing to capture diagonally.
    state = empty_state()
    put(state, (0, 0), Kind.ROOK, Color.WHITE, 5)
    put(state, (6, 7), Kind.PAWN, Color.BLACK, 1)
    put(state, (5, 7), Kind.PAWN, Color.WHITE, 1)
    result = apply_move(state, Move((0, 0), (1, 0)), FixedRandom(0.99))
    assert result.ended_by_chance
    assert state.end_reason == "stalemate"
    assert state.winner is Color.BLACK  # roll 0.99 >= 6/7


def test_battle_resets_quiet_turn_counter_even_on_failure():
    state = empty_state()
    put(state, (0, 0), Kind.KNIGHT, Color.WHITE, 3)
    put(state, (2, 1), Kind.ROOK, Color.BLACK, 5)
    put(state, (0, 7), Kind.KING, Color.WHITE, 4)
    state.quiet_turns = 30
    apply_move(state, Move((0, 0), (2, 1)), FixedRandom(0.9))
    assert state.quiet_turns == 0

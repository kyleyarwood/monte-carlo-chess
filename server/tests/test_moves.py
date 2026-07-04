from app.engine.models import Color, GameState, Kind, Move, Piece
from app.engine.moves import legal_moves, piece_moves


def empty_state() -> GameState:
    state = GameState(board=[[None] * 8 for _ in range(8)])
    return state


def put(state, sq, kind, color, power=1, has_moved=True):
    piece = Piece(kind, color, power, has_moved=has_moved)
    state.board[sq[0]][sq[1]] = piece
    return piece


def targets(state, sq):
    return {m.to_sq for m in piece_moves(state, sq)}


def test_initial_position_has_twenty_moves_per_side():
    state = GameState()
    assert len(legal_moves(state, Color.WHITE)) == 20
    assert len(legal_moves(state, Color.BLACK)) == 20


def test_knight_jumps_and_captures():
    state = empty_state()
    put(state, (4, 4), Kind.KNIGHT, Color.WHITE)
    put(state, (6, 5), Kind.PAWN, Color.BLACK)
    put(state, (2, 3), Kind.PAWN, Color.WHITE)
    expected = {(6, 5), (6, 3), (2, 5), (5, 6), (5, 2), (3, 6), (3, 2)}
    assert targets(state, (4, 4)) == expected


def test_sliders_stop_at_blockers():
    state = empty_state()
    put(state, (0, 0), Kind.ROOK, Color.WHITE)
    put(state, (0, 3), Kind.PAWN, Color.BLACK)
    put(state, (2, 0), Kind.PAWN, Color.WHITE)
    assert targets(state, (0, 0)) == {(0, 1), (0, 2), (0, 3), (1, 0)}


def test_king_can_move_into_attacked_square():
    # No check rules: the king may step onto a square a rook attacks.
    state = empty_state()
    put(state, (0, 4), Kind.KING, Color.WHITE)
    put(state, (7, 5), Kind.ROOK, Color.BLACK)
    assert (0, 5) in targets(state, (0, 4))
    assert (1, 5) in targets(state, (0, 4))


def test_pawn_double_push_only_from_start():
    state = empty_state()
    put(state, (1, 0), Kind.PAWN, Color.WHITE, has_moved=False)
    put(state, (3, 4), Kind.PAWN, Color.WHITE)
    assert targets(state, (1, 0)) == {(2, 0), (3, 0)}
    assert targets(state, (3, 4)) == {(4, 4)}


def test_pawn_captures_diagonally_only():
    state = empty_state()
    put(state, (3, 3), Kind.PAWN, Color.WHITE)
    put(state, (4, 3), Kind.PAWN, Color.BLACK)  # blocks the push
    put(state, (4, 4), Kind.PAWN, Color.BLACK)
    put(state, (4, 2), Kind.PAWN, Color.WHITE)
    assert targets(state, (3, 3)) == {(4, 4)}


def test_en_passant_offered_only_on_target_square():
    state = empty_state()
    put(state, (4, 4), Kind.PAWN, Color.WHITE)
    put(state, (4, 5), Kind.PAWN, Color.BLACK)
    state.en_passant_target = (5, 5)
    assert (5, 5) in targets(state, (4, 4))
    state.en_passant_target = None
    assert (5, 5) not in targets(state, (4, 4))


def test_promotion_generates_all_four_choices():
    state = empty_state()
    put(state, (6, 0), Kind.PAWN, Color.WHITE)
    moves = piece_moves(state, (6, 0))
    assert {m.promotion for m in moves} == {
        Kind.KNIGHT,
        Kind.BISHOP,
        Kind.ROOK,
        Kind.QUEEN,
    }


def test_castling_both_sides_when_clear():
    state = empty_state()
    put(state, (0, 4), Kind.KING, Color.WHITE, has_moved=False)
    put(state, (0, 0), Kind.ROOK, Color.WHITE, has_moved=False)
    put(state, (0, 7), Kind.ROOK, Color.WHITE, has_moved=False)
    castle_targets = targets(state, (0, 4))
    assert (0, 6) in castle_targets and (0, 2) in castle_targets


def test_castling_blocked_or_moved_rook():
    state = empty_state()
    put(state, (0, 4), Kind.KING, Color.WHITE, has_moved=False)
    put(state, (0, 0), Kind.ROOK, Color.WHITE, has_moved=True)
    put(state, (0, 7), Kind.ROOK, Color.WHITE, has_moved=False)
    put(state, (0, 5), Kind.BISHOP, Color.WHITE)
    castle_targets = targets(state, (0, 4))
    assert (0, 6) not in castle_targets and (0, 2) not in castle_targets


def test_castling_allowed_through_attacked_squares():
    # Check does not exist, so castling "through check" is legal.
    state = empty_state()
    put(state, (0, 4), Kind.KING, Color.WHITE, has_moved=False)
    put(state, (0, 7), Kind.ROOK, Color.WHITE, has_moved=False)
    put(state, (7, 5), Kind.ROOK, Color.BLACK)
    assert (0, 6) in targets(state, (0, 4))

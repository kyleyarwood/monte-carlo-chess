"""Move generation for Monte Carlo Chess.

Movement geometry is identical to standard chess, but there is no concept
of check: moves are never filtered for king safety, and castling only
requires an unmoved king and rook with empty squares between them.
"""

from __future__ import annotations

from .models import BOARD_SIZE, Color, GameState, Kind, Move, PROMOTION_KINDS

ROOK_DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
BISHOP_DIRS = ((1, 1), (1, -1), (-1, 1), (-1, -1))
KNIGHT_JUMPS = (
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2),
)


def on_board(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def legal_moves(state: GameState, color: Color) -> list[Move]:
    moves: list[Move] = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = state.board[row][col]
            if piece is not None and piece.color == color:
                moves.extend(piece_moves(state, (row, col)))
    return moves


def piece_moves(state: GameState, sq: tuple[int, int]) -> list[Move]:
    piece = state.piece_at(sq)
    if piece is None:
        return []
    if piece.kind is Kind.PAWN:
        return _pawn_moves(state, sq)
    if piece.kind is Kind.KNIGHT:
        return _step_moves(state, sq, KNIGHT_JUMPS)
    if piece.kind is Kind.BISHOP:
        return _slide_moves(state, sq, BISHOP_DIRS)
    if piece.kind is Kind.ROOK:
        return _slide_moves(state, sq, ROOK_DIRS)
    if piece.kind is Kind.QUEEN:
        return _slide_moves(state, sq, ROOK_DIRS + BISHOP_DIRS)
    return _step_moves(state, sq, ROOK_DIRS + BISHOP_DIRS) + _castle_moves(state, sq)


def _step_moves(
    state: GameState, sq: tuple[int, int], offsets: tuple[tuple[int, int], ...]
) -> list[Move]:
    piece = state.piece_at(sq)
    moves = []
    for dr, dc in offsets:
        row, col = sq[0] + dr, sq[1] + dc
        if not on_board(row, col):
            continue
        target = state.board[row][col]
        if target is None or target.color != piece.color:
            moves.append(Move(sq, (row, col)))
    return moves


def _slide_moves(
    state: GameState, sq: tuple[int, int], dirs: tuple[tuple[int, int], ...]
) -> list[Move]:
    piece = state.piece_at(sq)
    moves = []
    for dr, dc in dirs:
        row, col = sq[0] + dr, sq[1] + dc
        while on_board(row, col):
            target = state.board[row][col]
            if target is None:
                moves.append(Move(sq, (row, col)))
            else:
                if target.color != piece.color:
                    moves.append(Move(sq, (row, col)))
                break
            row, col = row + dr, col + dc
    return moves


def _pawn_moves(state: GameState, sq: tuple[int, int]) -> list[Move]:
    piece = state.piece_at(sq)
    direction = 1 if piece.color is Color.WHITE else -1
    start_row = 1 if piece.color is Color.WHITE else 6
    last_row = 7 if piece.color is Color.WHITE else 0
    row, col = sq
    moves = []

    def add(to_sq: tuple[int, int]) -> None:
        if to_sq[0] == last_row:
            for kind in PROMOTION_KINDS:
                moves.append(Move(sq, to_sq, promotion=kind))
        else:
            moves.append(Move(sq, to_sq))

    one_ahead = (row + direction, col)
    if on_board(*one_ahead) and state.piece_at(one_ahead) is None:
        add(one_ahead)
        two_ahead = (row + 2 * direction, col)
        if row == start_row and state.piece_at(two_ahead) is None:
            moves.append(Move(sq, two_ahead))

    for dc in (-1, 1):
        to_sq = (row + direction, col + dc)
        if not on_board(*to_sq):
            continue
        target = state.piece_at(to_sq)
        if target is not None and target.color != piece.color:
            add(to_sq)
        elif target is None and to_sq == state.en_passant_target:
            moves.append(Move(sq, to_sq))

    return moves


def _castle_moves(state: GameState, sq: tuple[int, int]) -> list[Move]:
    king = state.piece_at(sq)
    if king.has_moved:
        return []
    row = sq[0]
    moves = []
    for rook_col, between_cols, king_to in ((7, (5, 6), 6), (0, (1, 2, 3), 2)):
        rook = state.board[row][rook_col]
        if (
            rook is not None
            and rook.kind is Kind.ROOK
            and rook.color == king.color
            and not rook.has_moved
            and all(state.board[row][c] is None for c in between_cols)
        ):
            moves.append(Move(sq, (row, king_to)))
    return moves


def is_castle(state: GameState, move: Move) -> bool:
    piece = state.piece_at(move.from_sq)
    return (
        piece is not None
        and piece.kind is Kind.KING
        and abs(move.to_sq[1] - move.from_sq[1]) == 2
    )


def is_en_passant(state: GameState, move: Move) -> bool:
    piece = state.piece_at(move.from_sq)
    return (
        piece is not None
        and piece.kind is Kind.PAWN
        and move.to_sq == state.en_passant_target
        and move.from_sq[1] != move.to_sq[1]
    )

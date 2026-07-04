from models.colour import Colour
from models.posn import Posn
from models.vector import Vector

from typing import List, Optional

def is_on_board(*, board: 'models.board.Board', posn: Posn) -> bool:
    return 0 <= posn.row < board.BOARD_SIZE and 0 <= posn.col < board.BOARD_SIZE


def is_occupied(*, board: 'models.board.Board', posn: Posn) -> bool:
    return any(
        is_occupied_by_colour(board=board, posn=posn, colour=colour)
        for colour in Colour
    )


def is_occupied_by_colour(*, board: 'models.board.Board', posn: Posn, colour: Colour) -> bool:
    assert is_on_board(board=board, posn=posn), f"Posn {posn} is not on the board"
    piece_at_posn: Optional[Piece] = board.board[posn.row][posn.col]
    return piece_at_posn is not None and piece_at_posn.colour == colour


def is_clear_path(
    *, 
    board: 'models.board.Board', 
    posn1: Posn, 
    posn2: Posn, 
    allow_diagonal: bool = False, 
    allow_straight: bool = False
) -> bool:
    if posn1 == posn2:
        return True
    slope_row: int = (posn2.row - posn1.row)//max(abs(posn2.row - posn1.row), 1)
    slope_col: int = (posn2.col - posn1.col)//max(abs(posn2.col - posn1.col), 1)
    slope_vector: Vector = Vector(dx=slope_row, dy=slope_col)
    curr_posn: Posn = Posn(row=posn1.row, col=posn1.col)
    curr_posn += slope_vector
    print(curr_posn.row, curr_posn.col)
    while is_on_board(board=board, posn=curr_posn) and not is_occupied(board=board, posn=curr_posn) and curr_posn != posn2:
        curr_posn += slope_vector
    print(curr_posn.row, curr_posn.col, posn2.row, posn2.col)
    return curr_posn == posn2

def is_attacked_by_colour(*, board: 'models.board.Board', posn: Posn, colour: Colour) -> bool:
    row: List[Optional[Piece]]
    for row in board.board:
        piece: Optional[Piece]
        for piece in row:
            if piece is None or piece.colour != colour:
                continue
            if posn in piece.attacked_squares(board=board):
                return True
    return False

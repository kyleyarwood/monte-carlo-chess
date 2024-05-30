from models.colour import Colour
from models.posn import Posn

from typing import Optional

def is_on_board(*, board: 'models.board.Board', posn: Posn):
    return 0 <= posn.row < board.BOARD_SIZE and 0 <= posn.col < board.BOARD_SIZE


def is_occupied(*, board: 'models.board.Board', posn: Posn):
    return any(
        is_occupied_by_colour(board=board, posn=posn, colour=colour)
        for colour in Colour
    )


def is_occupied_by_colour(*, board: 'models.board.Board', posn: Posn, colour: Colour):
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
):
    if posn1 == posn2:
        return True
    slope_row: int = (posn2.row - posn1.row)//max(abs(posn2.row - posn1.row), 1)
    slope_col: int = (posn2.col - posn1.col)//max(abs(posn2.col - posn1.col), 1)
    slope_vector: Vector = Vector(dx=slope_row, dy=slope_col)
    curr_posn = Posn(posn1.row, posn1.col)
    while is_on_board(board=board, posn=curr_posn) and not is_occupied(board=board, posn=curr_posn) and curr_posn != posn2:
        curr_posn += slope_vector
    return curr_posn == posn2


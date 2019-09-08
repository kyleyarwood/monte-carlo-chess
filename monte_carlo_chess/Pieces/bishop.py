from .piece import Piece
from .. import utility


class Bishop(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour, 3, "P")

    # takes in the chessboard and the new position and returns
    # whether or not the piece can move to the new position legally
    def isValidMove(self, curr_posn, new_posn, board):
        return utility.clear_path(curr_posn, new_posn, board, False, True)

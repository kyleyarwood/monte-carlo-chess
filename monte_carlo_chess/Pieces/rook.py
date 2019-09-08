from .piece import Piece
from .. import utility


class Rook(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour, 5, "R")

    def isValidMove(self, curr_posn, new_posn, board):
        return utility.clear_path(curr_posn, new_posn, board, True, False)

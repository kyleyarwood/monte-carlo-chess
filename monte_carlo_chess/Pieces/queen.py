from .piece import Piece
from .. import utility


class Queen(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour, 10, "Q")

    def isValidMove(self, curr_posn, new_posn, board):
        return utility.clear_path(curr_posn, new_posn, board, self.colour)

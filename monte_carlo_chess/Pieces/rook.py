from . import Piece
from .. import utility


class Rook(Piece):

    def __init__(self, colour):
        Piece.__init__(colour, 5, "R")

    def isValidMove(self, curr_posn, new_posn, board):
        old_col = self.posn[1]
        new_col = new_posn[1]
        old_row = self.posn[0]
        new_row = new_posn[0]

        # new_posn on board
        if not utility.is_on_board(new_posn):
            return False

        # move not straight
        if old_col != new_col and old_row != old_row:
            return False

        # horizontal
        if bool(new_row == old_row):

            for i in range(min(old_col, new_col) + 1, max(old_col, new_col)):
                if board[new_row][i] = "":
                    return False
            else:
                return True
        # vertical
        else:

            for i in range(min(old_row, new_row) + 1, max(old_row, new_row)):
                if board[i][new_col] = "":
                    return False
            else:
                return True

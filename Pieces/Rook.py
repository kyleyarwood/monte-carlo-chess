from . import Piece


class Rook(Piece):

    # SHOULD NOT BE MERGED
    def __init__(self, colour, posn):
        Piece.__init__(colour, posn)
        self.power = 5

    def isValidMove(self, new_posn, board):
        old_col = self.posn[1]
        new_col = new_posn[1]
        old_row = self.posn[0]
        new_row = new_posn[0]

        WIDTH = len(board[0])
        HEIGHT = len(board)

        # make sure new_posn is on the board
        if new_row >= HEIGHT or new_row < 0 or new_col >= WIDTH or new_col < 0:
            return False

        horizontal = bool(new_row == old_row)
        vertical = bool(new_col == old_col)

        if horizontal:

            for i in range(min(old_col, new_col) + 1, max(old_col, new_col)):
                if board[new_row][i]:
                    return False
            else:
                return True

        elif vertical:

            for i in range(min(old_row, new_row) + 1, max(old_row, new_row)):
                if board[i][new_col]:
                    return False
            else:
                return True

        else:
            return False

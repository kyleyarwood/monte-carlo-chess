from .piece import Piece


class Bishop(Piece):

    def __init__(self, colour, posn):
        Piece.__init__(self, colour, posn, 3, "B")

    # takes in the chessboard and the new position and returns
    # whether or not the piece can move to the new position legally
    def isValidMove(self, new_posn, board):
        # defining for readability
        old_col = self.posn[1]
        new_col = new_posn[1]
        old_row = self.posn[0]
        new_row = new_posn[0]
        WIDTH = len(board[0])
        HEIGHT = len(board)

        # check that new_posn is on the board
        if new_row < 0 or new_row >= HEIGHT or new_col < 0 or new_col >= HEIGHT:
            return False

        # check for positive slope move
        pos_slope = bool(new_row - old_row == new_col - old_col)

        # check for negative slope move
        neg_slope = bool(new_row - old_row == -(new_col - old_col))

        min_row, max_row = min(old_row, new_row), max(old_row, new_row)
        min_col, max_col = min(old_col, new_col), max(old_col, new_col)

        # check to see if anything is in between old position and new position
        if pos_slope:

            for i in range(min_col + 1, max_col):
                for j in range(max_row - 1, min_row, -1):
                    if board[i][j]:
                        return False
            else:
                return True

        elif neg_slope:

            for i in range(min_col + 1, max_col):
                for j in range(min_row + 1, max_row):
                    if board[i][j]:
                        return False
            else:
                return True

        else:
            return False

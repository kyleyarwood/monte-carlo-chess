from .piece import Piece
from .. import utility
from math import abs


class King(Piece):

    def __init__(self, color):
        Piece.__init__(self, colour, 4, "K")

    def isValidMove(self, curr_posn, new_posn, board):

        if not is_on_board(new_posn) or same_colour_in_spot(new_posn):
            return False

        # move of distance one
        if abs(new_posn[1] - self.curr_posn[1]) + abs(new_posn[0] - self.curr_posn[0]) == 1:
            return True

        # castling

        # where the castling rook be
        if new_posn[1] == 2:
            target_rook_posn = [new_posn[0], 0]
        elif new_posn[1] == 6:
            target_rook_posn = [new_posn[0], 7]
        else:
            return False

        # must be rook to castle
        if not board[target_rook_posn] or board[target_rook_posn].name != "R":
            return False

        # both king and rook must have not moved
        if self.has_moved or board[target_rook_posn].has_moved:
            return False

        for col in range(min(curr_posn[1], target_rook_posn[1]) + 1, max(curr_posn[1], target_rook_posn[1]) - 1):
            # piece in the way
            if board[(new_posn[0], col)] or can_be_attacked((new_posn[0], col), board):
                return False

        return True

        def move(self, curr_posn, new_posn, board):

            if vaildMove(self, curr_posn, new_posn, board):
                # is castling
                if abs(new_posn[1] - self.curr_posn[1]) + abs(new_posn[0] - self.curr_posn[0]) != 1:
                    if new_posn[1] == 2:
                        target_rook_posn = [new_posn[0], 0]
                    elif new_posn[1] == 6:
                        target_rook_posn = [new_posn[0], 7]
                    else:
                        raise BadMoveError(
                            "Castling but King is not correct position")

                    if not board[target_rook_posn]:
                        raise raise BadMoveError("Castling but Rook is not correct position")

                    if not board[target_rook_posn].move(target_rook_posn, [target_rook_posn[0], 3 if val == 2 else 5], board):
                        raise raise BadMoveError("Castling but Rook can not be moved")

                self.has_moved = True
                return True
            else:
                return False

        def can_be_attacked(self, posn, board):

            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if board[(row, col)] and board[(row, col)].colour == "B" if val == "W" else "W" and board[(row, col)].isValidMove((row, col), posn, board)
                    return False
            return True

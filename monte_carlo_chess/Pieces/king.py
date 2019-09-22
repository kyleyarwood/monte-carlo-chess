from .piece import Piece
from .. import utility

# from math import abs
class King(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour, 4, "K")

    def is_valid_move(self, curr_posn, new_posn, board):

        if not utility.is_on_board(new_posn) or utility.same_colour_in_spot(new_posn)
            or self.can_be_attacked(new_posn, board):
            return False

        # position changes
        delta_x = abs(new_posn[1] - self.curr_posn[1])
        delta_y = abs(new_posn[0] - self.curr_posn[0])

        # move of distance one
        if (delta_x + delta_y <= 2) and (delta_x == 1 or delta_y == 1) and
            not utility.same_colour_in_spot(new_posn):
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

        for col in range(
            min(curr_posn[1], target_rook_posn[1]),
            max(curr_posn[1], target_rook_posn[1]) + 1,
        ):
            """special case for col = 1, since long castling has one spot that won't be occupied
            and we don't care if it's being attacked"""
            if col != 1 and self.can_be_attacked((new_posn[0], col), board):
                return False

            # piece in-between king and rook
            if (col != curr_posn[1] and col != target_rook_posn[1]) and board[(new_posn[0], col)]:
                return False

        return True

        def move(self, curr_posn, new_posn, board):

            if self.is_valid_move(self, curr_posn, new_posn, board):
                # is castling
                target_rook_posn = None
                if (
                    abs(new_posn[1] - self.curr_posn[1])
                    + abs(new_posn[0] - self.curr_posn[0])
                    != 1
                ):
                    if new_posn[1] == 2:
                        target_rook_posn = Posn(new_posn[0], 0)
                    elif new_posn[1] == 6:
                        target_rook_posn = Posn(new_posn[0], 7)
                    else:
                        #should never happen
                        raise BadMoveError("Castling but King is not correct position")

                    if not board[target_rook_posn]:
                        #should never happen
                        raise BadMoveError("Castling but Rook is not correct position")

                    if not board[target_rook_posn].move(
                        target_rook_posn,
                        Posn(target_rook_posn[0], 3 if val == 2 else 5),
                        board,
                    ):
                        raise BadMoveError("Castling but Rook can not be moved")
                board.move(target_rook_posn, Posn(target_rook_posn[0], 3 if val == 2 else 5))
                self.has_moved = True
                return True
            else:
                return False

        def can_be_attacked(self, posn, board):

            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if (
                        board[(row, col)] and board[(row, col)].colour == "B"
                        if self.colour == "W"
                        else "W"
                        and board[(row, col)].isValidMove((row, col), posn, board)
                    ):
                        return False
            return True

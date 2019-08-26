from .piece import Piece


class Pawn(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour, 1, "P")

    def isValidMove(self, new_posn, board):
        """
        implement en passant,
        double stepping on first move,
        and attacking diagonally, as well
        as regular moving and promotion
        """

        moving_direction = 1  # if piece is white, move up board

        if self.colour == "B":
            moving_direction = -1  # if piece is black, move down board

        if (
            new_posn[1] == self.posn[1]
            and new_posn[0] == self.posn[0] - moving_direction
        ):
            # regular move
            if board[new_posn[0]][new_posn[1]]:
                return False
            else:
                return True
        elif (
            abs(new_posn[1] - self.posn[1]) == 1
            and new_posn[0] == self.posn[0] - moving_direction
        ):
            # attacking a piece
            if board[new_posn[0]][new_posn[1]]:
                return True
            else:
                return False
        elif (
            not self.has_moved
            and new_posn[1] == self.posn[1]
            and new_posn[0] == self.posn[0] - 2 * moving_direction
        ):
            # double step on first move
            if (
                board[new_posn[0]][new_posn[1]]
                or board[new_posn[0] + moving_direction][new_posn[1]]
            ):
                return False
            else:
                return True
        elif False:
            # en passant
            # TODO implement this
            return False
        else:
            return False

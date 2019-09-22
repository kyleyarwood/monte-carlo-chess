from .piece import Piece
from .. import utility


class Knight(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour, 3, "N")

    def is_valid_move(self, curr_posn, new_posn, board):
        # euclidean distance squared between curr_posn and new_posn must be 5
        return (
            is_on_board(new_posn)
            and not utility.same_colour_in_spot(new_posn, board, self.colour)
            and (
                (new_posn[1] - self.curr_posn[1]) ** 2
                + (new_posn[0] - self.curr_posn[0]) ** 2
                == 5
            )
        )

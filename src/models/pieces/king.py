from models.colour import Colour
from models.posn import Posn
from models.pieces.piece import Piece
import models.util as util

class King(Piece):
    def __init__(self, colour: Colour, posn: Posn, power: int = 4):
        super().__init__(colour=colour, power=power, notation='K', posn=posn)

    def _is_valid_move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        if not super()._is_valid_move(new_posn=new_posn, board=board):
            return False
        row_diff: int = abs(new_posn.row - self.posn.row)
        col_diff: int = abs(new_posn.col - self.posn.col)
        if max(row_diff, col_diff) == 1:
            return True
        # handle castling
        return False

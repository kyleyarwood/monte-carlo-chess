from models.colour import Colour
from models.posn import Posn
from models.pieces.piece import Piece
import models.util as util

class Pawn(Piece):
    def __init__(self, colour: Colour, posn: Posn, power: int = 1):
        super().__init__(colour=colour, power=power, notation='P', posn=posn)

    def _is_valid_move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        if not super()._is_valid_move(new_posn=new_posn, board=board):
            return False
        # handle move by 1, move by 2, and en passant
        return False

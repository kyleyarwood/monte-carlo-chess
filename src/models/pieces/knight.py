from models.colour import Colour
from models.posn import Posn
from models.pieces.piece import Piece
import models.util as util

class Knight(Piece):
    def __init__(self, colour: Colour, posn: Posn, power: int = 3):
        super().__init__(colour=colour, power=power, notation='N', posn=posn)

    def _is_valid_move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        euclidean_distance_sqrd: int = (new_posn.row - self.posn.row)**2 + (new_posn.col - self.posn.col)**2
        return euclidean_distance_sqrd == 5 and super()._is_valid_move(new_posn=new_posn, board=board)

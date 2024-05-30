from models.colour import Colour
from models.posn import Posn
from models.pieces.piece import Piece
import models.util as util

class Queen(Piece):
    def __init__(self, colour: Colour, posn: Posn, power: int = 9):
        super().__init__(colour=colour, power=power, notation='Q', posn=posn)

    def _is_valid_move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        return util.is_clear_path(
            board=board,
            posn1=self.posn,
            posn2=new_posn,
            allow_diagonal=True,
            allow_straight=True,
        ) and super()._is_valid_move(new_posn=new_posn, board=board)

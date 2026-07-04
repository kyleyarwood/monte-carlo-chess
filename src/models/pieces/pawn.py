from models.colour import Colour
from models.posn import Posn
from models.pieces.piece import Piece
import models.util as util
from models.vector import Vector

from typing import List

class Pawn(Piece):
    def __init__(self, colour: Colour, posn: Posn, power: int = 1):
        super().__init__(colour=colour, power=power, notation='P', posn=posn)

    def _is_valid_move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        if not super()._is_valid_move(new_posn=new_posn, board=board):
            return False
        opp_colour: Colour = Colour.WHITE if self.colour == Colour.BLACK else Colour.BLACK
        left_vector: Vector = Vector(dx=0, dy=-1)
        right_vector: Vector = Vector(dx=0, dy=1)
        vector: Vector = Vector(dx=(-1 if self.colour == Colour.WHITE else 1), dy=0)
        if util.is_occupied_by_colour(board=board, posn=new_posn, colour=opp_colour):
            return new_posn == self.posn + vector + left_vector or new_posn == self.posn + vector + right_vector
        if new_posn == self.posn + vector or new_posn == self.posn + vector * 2 and not self.has_moved:
            return util.is_clear_path(board=board, posn1=self.posn, posn2=new_posn, allow_straight=True, allow_diagonal=False)
        # handle en passant, promotion 
        if new_posn == self.posn + vector + left_vector or new_posn == self.posn + vector + right_vector:
            ... #en passant
        return False

    def attacked_squares(self, *, board: 'models.board.Board') -> List[Posn]:
        row: int
        if self.colour == Colour.WHITE:
            row = self.posn.row - 1
        else:
            row = self.posn.row + 1
        col: int
        res: List[Posn] = []
        for col in (self.posn.col - 1, self.posn.col + 1):
            posn: Posn = Posn(row=row, col=col)
            if self._is_valid_move(new_posn=posn, board=board):
                res.append(posn)
        return res


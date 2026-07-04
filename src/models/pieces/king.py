from models.colour import Colour
from models.posn import Posn
from models.pieces.piece import Piece
from models.pieces.rook import Rook
from models.vector import Vector
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
        return self._is_valid_castle(new_posn=new_posn, board=board)

    def _is_valid_castle(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        if new_posn.row != self.posn.row or self.has_moved or abs(new_posn.col - self.posn.col) != 2:
            return False
        dcol: int = 1 if new_posn.col > self.posn.col else -1
        vector: Vector = Vector(dx=0, dy=dcol)
        curr_posn: Posn = Posn(row=self.posn.row, col=self.posn.col) + vector
        opp_colour: Colour = Colour.WHITE if self.colour == Colour.BLACK else Colour.BLACK
        while util.is_on_board(posn=curr_posn, board=board) and not util.is_occupied(posn=curr_posn, board=board):
            if util.is_attacked_by_colour(colour=opp_colour, board=board, posn=curr_posn):
                return False
            curr_posn += vector
        if not util.is_on_board(posn=curr_posn, board=board):
            return False
        piece: Piece = board.board[curr_posn.row][curr_posn.col]
        return piece.colour == self.colour and isinstance(piece, Rook) and not piece.has_moved


from models.posn import Posn
from models.pieces.piece import Piece

class Move:
    def __init__(self, *, old_posn: Posn, new_posn: Posn, piece: Piece):
        self.old_posn = old_posn
        self.new_posn = new_posn
        self.piece = piece

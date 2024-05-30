from models.colour import Colour
from models.posn import Posn
import models.util as util

class Piece:
    def __init__(self, *, colour: Colour, power: int, notation: str, posn: Posn):
        self.colour: Colour = colour
        self.power: int = power
        self.notation: str = notation
        self.posn: Posn = posn
        self.has_moved: bool = False

    def move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        if self._is_valid_move(new_posn=new_posn, board=board):
            self.has_moved = True
            self.posn = new_posn
            return True
        return False

    def _is_valid_move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        return util.is_on_board(board=board, posn=new_posn) and not util.is_occupied_by_colour(
            board=board, posn=new_posn, colour=self.colour
        )

    def __str__(self) -> str:
        if self.colour == Colour.WHITE:
            return self.notation.upper()
        return self.notation.lower()


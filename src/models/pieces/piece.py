from models.colour import Colour
from models.posn import Posn
import models.util as util

import random
from typing import List


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
            if self._is_attacking_move(new_posn=new_posn, board=board):
                self._attack(attacked_posn=new_posn, board=board, random=True)
            self.posn = new_posn
            return True
        return False

    def _attack(self, *, new_posn: Posn, board: 'models.board.Board', random: bool = True) -> None:
        attacked_piece: Piece = board.board[new_posn.row][new_posn.col]
        attack_probability: float = self.power/(self.power + attacked_piece.power)
        board[self.posn.row][self.posn.col] = None
        if not random or random.random() < attack_probability:
            board[new_posn.row][new_posn.col] = self
            self.power += attacked_piece.power
        else:
            attacked_piece.power += self.power

    def _is_attacking_move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        opp_colour: Colour = Colour.WHITE if self.colour == Colour.BLACK else Colour.BLACK
        return util.is_occupied_by_colour(board=board, posn=new_posn, colour=opp_colour)

    def _is_valid_move(self, *, new_posn: Posn, board: 'models.board.Board') -> bool:
        return util.is_on_board(board=board, posn=new_posn) and not util.is_occupied_by_colour(
            board=board, posn=new_posn, colour=self.colour
        )

    def __str__(self) -> str:
        if self.colour == Colour.WHITE:
            return self.notation.upper()
        return self.notation.lower()

    def attacked_squares(self, *, board: 'models.board.Board') -> List[Posn]:
        res: List[Posn] = []
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                posn: Posn = Posn(row=i, col=col)
                if self._is_valid_move(new_posn=posn, board=board):
                    res.append(posn)
        return res

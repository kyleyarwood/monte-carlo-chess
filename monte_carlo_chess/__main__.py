from board import Board
from Pieces.piece import Piece

p = Piece("W", [1, 1], 5, "B")
b = Board()
b[1, 1] = p

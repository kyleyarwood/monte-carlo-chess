import pytest
from models.colour import Colour
from models.pieces.pawn import Pawn
from models.posn import Posn
from models.board import Board  # Make sure to replace with the actual import if available
import models.util as util

# Test cases
class TestUtils:
    def setup_method(self):
        self.board = Board()

    def test_is_on_board__posn_within_board(self):
        posn = Posn(row=4, col=5)
        assert util.is_on_board(board=self.board, posn=posn) == True

    def test_is_on_board__posn_outside_board_row(self):
        posn = Posn(row=8, col=5)
        assert util.is_on_board(board=self.board, posn=posn) == False

    def test_is_on_board__posn_outside_board_col(self):
        posn = Posn(row=4, col=8)
        assert util.is_on_board(board=self.board, posn=posn) == False

    def test_is_on_board__posn_negative_row(self):
        posn = Posn(row=-1, col=5)
        assert util.is_on_board(board=self.board, posn=posn) == False

    def test_is_on_board__posn_negative_col(self):
        posn = Posn(row=4, col=-1)
        assert util.is_on_board(board=self.board, posn=posn) == False

    def test_is_occupied_by_colour__occupied(self):
        posn = Posn(row=4, col=5)
        piece = Pawn(colour=Colour.WHITE, posn=posn)
        self.board.board[posn.row][posn.col] = piece
    
        assert util.is_occupied_by_colour(board=self.board, posn=posn, colour=Colour.WHITE) == True

    def test_is_occupied_by_colour_not_occupied(self):
        posn = Posn(row=4, col=5)
        self.board.board[posn.row][posn.col] = None
        assert util.is_occupied_by_colour(board=self.board, posn=posn, colour=Colour.WHITE) == False

    def test_is_occupied_by_colour_wrong_colour(self):
        posn = Posn(row=4, col=5)
        piece = Pawn(colour=Colour.WHITE, posn=posn)
        self.board.board[posn.row][posn.col] = piece
    
        assert util.is_occupied_by_colour(board=self.board, posn=posn, colour=Colour.BLACK) == False

    def test_is_occupied_by_colour_outside_board(self):
        posn = Posn(row=8, col=5)
    
        with pytest.raises(AssertionError):
            util.is_occupied_by_colour(board=self.board, posn=posn, colour=Colour.WHITE)

if __name__ == "__main__":
    pytest.main()


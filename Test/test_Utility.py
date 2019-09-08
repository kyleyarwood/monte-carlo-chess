import unittest

from monte_carlo_chess import utility
from monte_carlo_chess.posn import Posn
import monte_carlo_chess.config as config


class test_utiliity(unittest.TestCase):
    def test_is_on_board_row_neg(self):
        row = -1
        posn = Posn(row, config.BOARD_SIZE // 2)
        self.assertFalse(utility.is_on_board(posn))

    def test_is_on_board_row_too_large(self):
        row = config.BOARD_SIZE
        posn = Posn(row, config.BOARD_SIZE // 2)
        self.assertFalse(utility.is_on_board(posn))

    def test_is_on_board_col_neg(self):
        col = -1
        posn = Posn(config.BOARD_SIZE // 2, col)
        self.assertFalse(utility.is_on_board(posn))

    def test_is_on_board_col_too_large(self):
        col = config.BOARD_SIZE
        posn = Posn(config.BOARD_SIZE // 2, col)
        self.assertFalse(utility.is_on_board(posn))

    def test_is_on_board_correct(self):
        posn = Posn(config.BOARD_SIZE // 2, config.BOARD_SIZE // 2)
        self.assertTrue(utility.is_on_board(posn))

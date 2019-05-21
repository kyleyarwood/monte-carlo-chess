import unittest

from monte_carlo_chess.board import Board


class test_board(unittest.TestCase):
    def test_stuff(self):
        assert Board()


if __name__ == '__main__':
    unittest.main()

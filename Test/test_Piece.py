import unittest

from monte_carlo_chess.board import Board
from monte_carlo_chess.Pieces.piece import Piece


class test_Piece(unittest.TestCase):
    def test_load(self):
        result = Piece("W", [1, 1], 5, "B")

    # name must be W or B
    def test_name_not_W_or_B(self):
        colour = "X"
        self.assertRaises(ValueError, Piece, colour, [1, 1], 5, "B")

    def test_name_W(self):
        colour = "W"
        result = Piece(colour, [1, 1], 5, "B")
        self.assertEqual(result.colour, "W")

    def test_name_B(self):
        colour = "B"
        result = Piece(colour, [1, 1], 5, "B")
        self.assertEqual(result.colour, "B")

    # posin must have two ints

    def test_posin_no_lenth(self):
        posin = 42
        self.assertRaises(TypeError, Piece, "W", posin, 5, "B")

    def test_posin_length_too_long(self):
        posin = [1, 2, 3]
        self.assertRaises(ValueError, Piece, "W", posin, 5, "B")

    def test_posin_length_too_short(self):
        posin = [1]
        self.assertRaises(ValueError, Piece, "W", posin, 5, "B")

    def test_posin_no_index(self):
        posin = {1, 2}
        self.assertRaises(TypeError, Piece, "W", posin, 5, "B")

    def test_posin_float(self):
        posin = [1.5, 1.5]
        self.assertRaises(ValueError, Piece, "W", posin, 5, "B")

    def test_posin_posin_negative(self):
        pass

    def test_posin_posin_out_of_range(self):
        pass

    def test_posin_length_2(self):
        posin = [1, 1]
        result = Piece("W", posin, 5, "B")
        self.assertEqual(result.posin, posin)

    # power must be an postive int

    def test_power_not_int(self):
        power = 5.1
        self.assertRaises(TypeError, Piece, "W", [1, 1], power, "B")

    def test_power_non_not_negtive(self):
        power = -5
        self.assertRaises(ValueError, Piece, "W", [1, 1], power, "B")

    def test_power_int(self):
        power = 5
        result = Piece("W", [1, 1], power, "B")
        self.assertEqual(result.power, power)

    # name must be an character

    def name_not_str(self):
        name = 1
        self.assertRaises(AssertionError, Piece, "W", [1, 1], 5, name)

    def name_not_empty_string(self):
        name = ""
        self.assertRaises(AssertionError, Piece, "W", [1, 1], 5, name)

    def name_not_empty_too_long(self):
        name = "BA"
        self.assertRaises(AssertionError, Piece, "W", [1, 1], 5, name)

    def test_power_character_upper(self):
        name = "B"
        result = Piece("W", [1, 1], 5, name)
        self.assertEqual(result.name, name.lower())

    def test_power_character_lower(self):
        name = "b"
        result = Piece("W", [1, 1], 5, name)
        self.assertEqual(result.name, name.lower())

    # vaildMove raises NotImplementedError

    def test_vaildmove_NotImplementedError(self):
        result = Piece("W", [1, 1], 5, "B")
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(NotImplementedError):
            result.vaildMove([1, 1], Board())


if __name__ == '__main__':
    unittest.main()

from monte_carlo_chess import utility
from monte_carlo_chess.posn import Posn

import pdb


class Piece:
    def __init__(self, colour, power, name):
        if not colour.upper() == "W" and not colour == "B".upper():
            raise ValueError("name must be either 'W' or 'B'")

        if not isinstance(power, int):
            raise TypeError("power must be an int")

        if power <= 0:
            raise ValueError("power must be positive")

        if not isinstance(name, str):
            TypeError("name must be a str")

        if not len(name) == 1:
            ValueError("name must be an character")

        self.colour = colour.upper()
        self.power = power
        self.name = name.upper()
        self.has_moved = False

    def move(self, curr_posn: Posn, new_posn: Posn, board):
        if (
            not utility.same_colour_in_spot(new_posn, board, self.colour) 
            and self.is_valid_move(curr_posn, new_posn, board)
        ):
            self.has_moved = True
            return True
        else:
            return False

    def is_valid_move(self, curr_posn, new_posn, board):
        raise NotImplementedError

    def __str__(self, powerLevel=False):
        """
        Stringify the piece.

        Returns the piece name or powerLevel, with white being uppcase

        Args:
            powerLevel (bool): Whether the powerLevel should be returned

        Returns:
            str: description

        """

        if powerLevel:
            raise ValueError("powerLevel must be less than 100")
            return str(self.power)
        else:
            if self.colour == "W":
                return self.name.upper()
            else:
                return self.name.lower()

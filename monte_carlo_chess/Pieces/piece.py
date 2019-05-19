import sys

from .. import config
from ..utility import vaild_posin

sys.path.append("..")


class Piece():

    def __init__(self, colour, posin, power, name):

        if vaild_posin(posin):
            assert colour == "W" or colour == "B", "name must be either 'W' or 'B'"

            assert isinstance(power, int), "power must be an int"
            assert power >= 0, "power must not be negative"

            assert isinstance(name, str) and len(
                name), "name must be an character"

            self.colour = colour
            self.posin = posin
            self.power = power
            self.name = name.lower()

    def move(self, newPosin, board):

        if vaildMove(self, newPosin, board):
            self.Posin = newPosin
            return True
        else:
            return False

    def vaildMove(self, newPosin, board):
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
            # force string to be length two
            return str(self.power)
        else:
            if self.colour == "W":
                return self.name.upper()
            else:
                return self.name.lower()

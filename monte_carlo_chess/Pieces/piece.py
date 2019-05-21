class Piece():

    def __init__(self, colour, posin, power, name):
        print(dir())
        if not validate_posn(posin):
            raise Exception()

        if not colour == "W" and not colour == "B":
            raise ValueError("name must be either 'W' or 'B'")

        if not isinstance(power, int):
            raise TypeError("power must be an int")

        if power <= 0:
            raise ValueError("power must not be postive")

        if not isinstance(name, str):
            TypeError("name must be a str")

        if not len(name) == 1:
            ValueError("name must be an character")

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

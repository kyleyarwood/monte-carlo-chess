class Piece():

    def __init__(self, colour, power, name):

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
        self.power = power
        self.name = name.upper()
        self.has_moved = False

    def move(self, curr_posn, new_posn, board):

        if vaildMove(self, curr_posn, new_posn, board):
            self.has_moved = True
            return True
        else:
            return False

    def vaildMove(self, curr_posn, new_posn, board):
        raise NotImplementedError

    def is_on_board(posn):
        if validate_posn(posn):
            if posn[0] in range(config.BOARD_SIZE) and posn[1] in range(config.BOARD_SIZE):
                return True
            else:
                return False

    def same_colour_in_spot(posn, board):
        if board[posn] or board[posn].colour != self.colour:
            return True
        return False

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


class BadMoveError(Exception):
    "Move not possible"
    pass

class Piece():

    def __init__(self, colour, posn, power, name):
        assert len(name) == 1, "The length of the name must be only one character"
        self.colour = colour
        self.posn = posn
        self.power = power
        self.name = name
        self.has_moved = False

    def move(self, new_posn, board):
        if vaildMove(self, new_posn, board):
            self.posn = new_posn
            self.has_moved = True
            return True
        else:
            return False

    def vaildMove(self, new_posn, board):
        raise NotImplementedError

    def __str__(self, power_level=False):
        if power_level:
            # force string to be length two
            return str(self.power)
        else:
            if self.colour == "W":
                return self.name.upper()
            else:
                return self.name.lower()

class Piece():

    def __init__(self, colour, posn, power, name):
        assert len(name) == 1, "The length of the name must be only one character"
        self.colour = colour
        self.posn = posn
        self.power = power
        self.name = name

    def move(self, newPosn, board):
        if vaildMove(self, newPosn, board):
            self.posn = newPosn
            return True
        else:
            return False

    def vaildMove(self, newPosn, board):
        raise NotImplementedError

    def __str__(self, powerLevel=False):
        if powerLevel:
            # force string to be length two
            return str(self.power)
        else:
            if self.colour == "W":
                return self.name.upper()
            else:
                return self.name.lower()

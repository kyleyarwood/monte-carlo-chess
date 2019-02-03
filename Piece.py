class Piece():

    def __init__(self, colour, posn, power, name):
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

    def __str__(self, powerLevel = False):
        if powerLevel:
            return str(self.power)
        else:
            if self.colour == "white":
                return self.name.upper()
            else:
                return self.name.lower()

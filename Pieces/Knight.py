class Knight(Piece):
    def __init__(self, colour, posn):
        Piece.__init__(self, colour, posn, 3, "N")

    def isValidMove(self, new_posn, board):
        if (new_posn[1] - self.posn[1])**2 + (new_posn[0] - self.posn[0])**2 == 5:
            return True
        else:
            return False


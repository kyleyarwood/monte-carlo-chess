import Piece


class Pawn(Piece):

    def __init__(self, colour, posn):
        Piece.__init__(colour, posn)
        self.power = 1
        self.isFirstMove = True

    def isValidMove(self, newPosn):
        '''
        implement en passant,
        double stepping on first move,
        and attacking diagonally, as well
        as regular moving and promotion
        '''

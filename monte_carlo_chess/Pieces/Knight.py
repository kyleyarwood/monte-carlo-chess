class Knight(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour, 3, "N")

    def isValidMove(self, curr_posn, new_posn, board):
        if is_on_board(new_posn) and not same_colour_in_spot(new_posn) and (new_posn[1] - self.curr_posn[1])**2 + (new_posn[0] - self.curr_posn[0])**2 == 5:
            return True
        else:
            return False

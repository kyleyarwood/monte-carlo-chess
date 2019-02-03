class Bishop(Piece):

    def __init__(self, colour, posn):
        Piece.__init(colour, posn)
        self.power = 3

    #takes in the chessboard and the new position and returns
    #whether or not the piece can move to the new position legally
    def isValidMove(self, board, newPosn):
        #defining for readability
        oldCol = self.posn[1]
        newCol = newPosn[1]
        oldRow = self.posn[0]
        newRow = newPosn[0]
        WIDTH = len(board[0])
        HEIGHT = len(board)

        #check that newPosn is on the board
        if newRow < 0 or newRow >= HEIGHT or newCol < 0 or newCol >= HEIGHT:
            return False

        #check for positive slope move
        posSlope = bool(newRow - oldRow == newCol - oldCol)

        #check for negative slope move
        negSlope = bool(newRow - oldRow == -(newCol - oldCol))


        minRow, maxRow = min(oldRow, newRow), max(oldRow, newRow)
        minCol, maxCol = min(oldCol, newCol), max(oldCol, newCol)


        #check to see if anything is in between old position and new position
        if posSlope:

            for i in range(minCol + 1, maxCol):
                for j in range(maxRow - 1, minRow, -1):
                    if board[i][j]:
                        return False
            else:
                return True
        
        elif negSlope:
        
            for i in range(minCol + 1, maxCol):
                for j in range(minRow + 1, maxRow):
                    if board[i][j]:
                        return False
            else:
                return True

        else:
            return False
        

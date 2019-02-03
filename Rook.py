class Rook(Piece):

    def __init__(self, colour, posn):
        Piece.__init__(colour, posn, 5, "R")

    def isValidMove(self, board, newPosn):
        oldCol = self.posn[1]
        newCol = newPosn[1]
        oldRow = self.posn[0]
        newRow = newPosn[0]

        WIDTH = len(board[0])
        HEIGHT = len(board)

        #make sure newPosn is on the board
        if newRow >= HEIGHT or newRow < 0 or newCol >= WIDTH or newCol < 0:
            return False

        horizontal = bool(newRow == oldRow)
        vertical = bool(newCol == oldCol)

        if horizontal:
        
            for i in range(min(oldCol, newCol) + 1, max(oldCol, newCol)):
                if board[newRow][i]:
                    return False
            else:
                return True
        
        elif vertical:

            for i in range(min(oldRow, newRow) + 1, max(oldRow, newRow)):
                if board[i][newCol]:
                    return False
            else:
                return True
        
        else:
            return False



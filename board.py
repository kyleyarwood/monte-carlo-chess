from random import random
Class Board():

    BOARD_SIZE = 8

	def __init__(self, colour,Posin):
        self.chessBoard = [[""] * BOARD_SIZE] * BOARD_SIZE
        self.players = []

    def move(self, currPosin,newPosin):
        """ Paramters: Takes the current location of a peice and new location of the pieace
            Return: a list on whether the move was successful, if there is an attack whether the attack was successful parameters
        """
        assert len(currPosin) = 2, "currPosin should have length 2"
        assert len(newPosin) = 2, "newPosin should have length 2"

        if chessBoard[currPosin[0]][currPosin[1]].move(newPosin,self):
            if chessBoard[newPosin[0]][newPosin[1]] == "":
                #Successfully moved to empty square
                chessBoard[newPosin[0]][newPosin[1]] = chessBoard[currPosin[0]][currPosin[1]]
                chessBoard[currPosition[0]][currPosition[1]] = ""
                return [True,None]
            else:
                if self.attack(chessBoard[currPosin[0]][currPosin[1]],newPosin[0]][newPosin[1]):
                    #Successfully moved to non-square and won
                    newPosin[0]][newPosin[1] = ""
                    newPosin[0]][newPosin[1] = piece
                    chessBoard[currPosin[0]][currPosin[1]] = ""
                    return [True,True]
                else:
                    #Successfully moved to non-square and lose
                    chessBoard[currPosin[0]][currPosin[1]] = ""
                    return [True,False]

        else:
            #Invaild move
            return [False,None]

    def setup():
        pass

    def attack(self, attackerPosin,defenderPosin):
        probWin = attacker.power / (attacker.power + defender.power)
        if random() < probWin:
            #attacker won
            attacker.power += defender.power
            self.delete(defender)
            return True
        else:
            #attacker lost
            defender.power += attacker.power
            self.delete(attacker)
            return False

    def __str__(self,powerlevel=False):
        boardStr = ""
        for i in self.chessBoard:
            row = ""
            for j in i:
                if j == "":
                    row += " "
                else:
                    row += str(j,powerlevel)
            row += "/n"
            boardSt += row
        return boardSt

from random import random


class Board():
    BOARD_SIZE = 8

    def __init__(self):
        self.chessBoard = [
            ["" for i in range(self.BOARD_SIZE)] for i in range(self.BOARD_SIZE)]
        self.players = []

    def move(self, currPosin, newPosin):
        """ Parameters: Takes the current location of a piece and new location of the piece
            Return: a list on whether the move was successful, if there is an attack whether the attack was successful parameters
        """
        assert len(currPosin) == 2, "currPosin should have length 2"
        assert len(newPosin) == 2, "newPosin should have length 2"

        if chessBoard[currPosin[0]][currPosin[1]].move(newPosin, self):
            if chessBoard[newPosin[0]][newPosin[1]] == "":
                # Successfully moved to empty square
                chessBoard[newPosin[0]][newPosin[1]
                                        ] = chessBoard[currPosin[0]][currPosin[1]]
                chessBoard[currPosition[0]][currPosition[1]] = ""
                return [True, None]
            else:
                if self.attack(chessBoard[currPosin[0]][currPosin[1]], newPosin):
                    # Successfully moved to non-empty square and won
                    chessBoard[newPosin[0]][newPosin[1]] = piece
                    chessBoard[currPosin[0]][currPosin[1]] = ""
                    return [True, True]
                else:
                    # Successfully moved to non-square and lose
                    chessBoard[currPosin[0]][currPosin[1]] = ""
                    return [True, False]

        else:
            # Invaild move
            return [False, None]

    def setup():
        pass

    def attack(self, attackerPosin, defenderPosin):
        """Determines which piece wins and deltes the loser
        """
        probWin = attacker.power / (attacker.power + defender.power)
        if random() < probWin:
            # attacker won
            attacker.power += defender.power
            self.delete(defender)
            return True
        else:
            # attacker lost
            defender.power += attacker.power
            self.delete(attacker)
            return False

    def __str__(self, powerlevel=False):
        """Print the board. By default, prints the piece names. If powerlevel is True, next prints the power level.
        """
        # TODO: allow powerlevels greater than 9
        letters = list(map(lambda x: chr(97 + x), range(self.BOARD_SIZE)))

        board_str = ""
        board_str += "  " + \
            str("".join(map(lambda x: x + " ", letters))) + "\n"
        board_str += " " + "-" * 17 + "\n"  # abstract -- board sizes greater than 9

        for row, i in zip(reversed(self.chessBoard), range(len(self.chessBoard) + 1, 1, -1)):
            row_str = str(i) + "|"
            for col, j in zip(row, letters):
                if col == "":
                    row_str += " |"
                else:
                    row_str += col.__str__(powerlevel) + "|"
            row_str += str(i)
            board_str += row_str + "\n"
            board_str += " " + "-" * 17 + "\n"
        board_str += "  " + \
            str("".join(map(lambda x: x + " ", letters)))
        return board_str

    def __getitem__(self, Posin):
        return self.chessBoard[Posin[0]][Posin[1]]

    def __setitem__(self, Posin, piece):
        self.chessBoard[Posin[0]][Posin[1]] = piece

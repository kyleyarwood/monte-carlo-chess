from random import random


class Board():
    BOARD_SIZE = 8

    def __init__(self):
        self.chessBoard = [
            ["" for i in range(self.BOARD_SIZE)] for i in range(self.BOARD_SIZE)]
        self.players = []

    def move(self, curr_posn, new_posn):
        """ Parameters: Takes the current location of a piece and new location of the piece
            Return: a list on whether the move was successful, if there is an attack whether the attack was successful parameters
        """
        assert len(curr_posn) == 2, "curr_posn should have length 2"
        assert len(new_posn) == 2, "new_posn should have length 2"

        if chessBoard[curr_posn[0]][curr_posn[1]].move(new_posn, self):
            if chessBoard[new_posn[0]][new_posn[1]] == "":
                # Successfully moved to empty square
                chessBoard[new_posn[0]][new_posn[1]
                                        ] = chessBoard[curr_posn[0]][curr_posn[1]]
                chessBoard[curr_posn[0]][curr_posn[1]] = ""
                return [True, None]
            else:
                if self.attack(chessBoard[curr_posn[0]][curr_posn[1]], new_posn):
                    # Successfully moved to non-empty square and won
                    chessBoard[new_posn[0]][new_posn[1]] = piece
                    chessBoard[curr_posn[0]][curr_posn[1]] = ""
                    return [True, True]
                else:
                    # Successfully moved to non-empty square and lost
                    chessBoard[curr_posn[0]][curr_posn[1]] = ""
                    return [True, False]

        else:
            # Invalid move
            return [False, None]

    def setup():
        pass

    def attack(self, attacker, defender):
        """Determines which piece wins and deletes the loser
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

    def __getitem__(self, posn):
        return self.chessBoard[posn[0]][posn[1]]

    def __setitem__(self, posn, piece):
        self.chessBoard[posn[0]][posn[1]] = piece

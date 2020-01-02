from random import random
from .config import BOARD_SIZE
from . import utility
from .posn import Posn

from .Pieces.bishop import Bishop
from .Pieces.king import King
from .Pieces.knight import Knight
from .Pieces.pawn import Pawn

from .Pieces.queen import Queen
from .Pieces.rook import Rook

HOME_ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class Board:
    def __init__(self):
        self.chessBoard = [
            [None for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)
        ]
        self.player_turn = "W"
        self.en_passanted_posn = None #if the last move was en passant, where did it occur

    def move(self, curr_posn, new_posn):
        """ Parameters: Takes the current location of a piece and new location of the piece
            Returns: a list on whether the move was successful, if there is an attack whether the attack was successful
        """

        if self.chessBoard[curr_posn[0]][curr_posn[1]] is not None and self.chessBoard[
            curr_posn[0]
        ][curr_posn[1]].move(curr_posn, new_posn, self):
            if self.chessBoard[new_posn[0]][new_posn[1]] == None:
                # Successfully moved to empty square
                self.chessBoard[new_posn[0]][new_posn[1]] = piece
                self.chessBoard[curr_posn[0]][curr_posn[1]] = None
                return [True]
            else:
                if self.attack(piece, self.chessBoard[new_posn[0]][new_posn[1]]):
                    # Successfully moved to non-empty square and won
                    self.chessBoard[new_posn[0]][new_posn[1]] = piece
                    self.chessBoard[new_posn[0]][new_posn[1]].posn = new_posn
                    self.chessBoard[curr_posn[0]][curr_posn[1]] = None
                    return [True, True]
                else:
                    # Successfully moved to non-empty square and lost
                    self.chessBoard[curr_posn[0]][curr_posn[1]] = None
                    return [True, False]

        else:
            # Invalid move
            return [False]

    def turn(self, curr_posn: Posn, new_posn: Posn):
        if not utility.is_on_board(curr_posn):
            raise IndexError(
                f"Board has size {BOARD_SIZE}. curr_posn is not chessBoard"
            )

        if not utility.is_on_board(new_posn):
            raise IndexError(
                f"Board has size {BOARD_SIZE}. new_posn is not chessBoard"
            )

        if chessBoard[curr_posn[0]][curr_posn[1]] is None:
            raise ValueError(f"({curr_posn[0]},{curr_posn[1]}) is empty.")

        if chessBoard[curr_posn[0]][curr_posn[1]].colour != self.player_turn:
            # Expand colour name?
            raise ValueError(
                f"The piece at ({curr_posn[0]},{curr_posn[1]}) is {chessBoard[curr_posn[0]][curr_posn[1]].colour}, it is {self.player_turn}'s turn to move'"
            )

        piece = curr_posn

        if self.player_turn == "W":
            self.player_turn = "B"
        elif self.player_turn == "B":
            self.player_turn = "W"
        else:
            pass
            # raise error invalid player_turn

    def setup(self):
        for i in range(0, BOARD_SIZE):
            self.chessBoard[0][i] = HOME_ROW[i]("W")
            self.chessBoard[1][i] = Pawn("W")
            self.chessBoard[BOARD_SIZE - 1][i] = HOME_ROW[i]("B")
            self.chessBoard[BOARD_SIZE - 2][i] = Pawn("B")
        print(self)

    def attack(self, attacker, defender):
        """ Deciding if the attacking piece wins. The winner's powerlevel is incremnted by the loser's powerlevel The probabilities that attacking piece is the attacker's power / (attacker's power + defender's power)

            Parameters:
                attacker(Piece) : Piece that is attacking (ie moving to the postion of the defending piece)
                defender(Piece) : Piece that defending (ie piece that is at the postion that the attacking piece is moving to)

            Returns:
                bool : True if the attacker wins, False if the defender wins
        """
        probWin = attacker.power / (attacker.power + defender.power)
        if random() < probWin:
            # attacker won
            attacker.power += defender.power
            return True
        else:
            # attacker lost
            defender.power += attacker.power
            return False

    def __str__(self, powerlevel=False) -> str:
        """Print the board. By default, prints the piece names. If powerlevel is True, next prints the power level.
        """
        # TODO: allow powerlevels greater than 9
        letters = list(map(lambda x: chr(97 + x), range(BOARD_SIZE)))

        board_str = ""
        board_str += "  " + str("".join(map(lambda x: x + " ", letters))) + "\n"
        board_str += " " + "-" * 17 + "\n"  # abstract -- board sizes greater than 9

        for row, i in zip(
            reversed(self.chessBoard), range(len(self.chessBoard), 0, -1)
        ):
            row_str = str(i) + "|"
            for col, j in zip(row, letters):
                if not col:
                    row_str += " |"
                else:
                    row_str += col.__str__(powerlevel) + "|"
            row_str += str(i)
            board_str += row_str + "\n"
            board_str += " " + "-" * 17 + "\n"
        board_str += "  " + str("".join(map(lambda x: x + " ", letters)))
        return board_str

    def __getitem__(self, posn: Posn):
        """ Gets piece from posn on chessBoard

            Parameters:
                posn(Posn) : Position of piece to be returned

            Returns:
                piece : The peice which is selected

            Raises:
                IndexError: If the posn is not on the board
        """
        if utility.is_on_board(posn):
            return self.chessBoard[posn.row][posn.col]
        raise IndexError("Board has size " + str(BOARD_SIZE))

    def __setitem__(self, posn: Posn, piece):
        """ Places piece on chessBoard at posn

            Parameters:
                posn(Posn) : Position of piece to be deleted
                piece(Piece) : Piece that will be placed

            Returns:
                bool : Return True if successful

            Raises:
                IndexError: If the posn is not on the board
        """
        if utility.is_on_board(posn):
            self.chessBoard[posn[0]][posn[1]] = piece
            return True
        raise IndexError("Board has size " + str(BOARD_SIZE))

    def __delitem__(self, posn: Posn):
        """ Deletes piece on board, by setting posn to None.

            Parameters:
                posn(Posn) : Position of piece to be deleted

            Returns:
                bool : Return True if successful

            Raises:
                IndexError: If the posn is not on the board
        """
        if utility.is_on_board(posn):
            self.chessBoard[posn[0]][posn[1]] = None
            return True
        raise IndexError("Board has size " + str(BOARD_SIZE))

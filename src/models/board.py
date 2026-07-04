from models.colour import Colour
from models.move import Move
from models.pieces.bishop import Bishop
from models.pieces.piece import Piece
from models.pieces.king import King
from models.pieces.knight import Knight
from models.pieces.pawn import Pawn
from models.pieces.queen import Queen
from models.pieces.rook import Rook
from models.posn import Posn
from typing import List, Optional, Type

class Board:
    BOARD_SIZE = 8

    def __init__(self):
        self.board: List[List[Optional[Piece]]] = self._generate_board()
        self.moves: List[Move] = []


    def _generate_board(self) -> List[List[Optional[Piece]]]:
        board: List[List[Optional[Piece]]] = [[None for _ in range(Board.BOARD_SIZE)] for __ in range(Board.BOARD_SIZE)]
        # Pawns
        col: int
        for col in range(Board.BOARD_SIZE):
            black_posn: Posn = Posn(row=1, col=col)
            board[1][col] = Pawn(colour=Colour.BLACK, posn=black_posn)
            white_posn: Posn = Posn(row=6, col=col)
            board[6][col] = Pawn(colour=Colour.WHITE, posn=white_posn)
        # Pieces
        PieceType: Type[Piece]
        for col, PieceType in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            black_posn: Posn = Posn(row=0, col=col)
            board[0][col] = PieceType(colour=Colour.BLACK, posn=black_posn)
            white_posn: Posn = Posn(row=7, col=col)
            board[7][col] = PieceType(colour=Colour.WHITE, posn=white_posn)
        return board

    def move(self, old_posn: Posn, new_posn: Posn) -> bool:
        assert self.board[old_posn.row][old_posn.col], f"No piece at {old_posn}"
        piece: Piece = self.board[old_posn.row][old_posn.col]
        if piece.move(new_posn=new_posn, board=self):
            self.board[new_posn.row][new_posn.col] = piece
            self.board[old_posn.row][old_posn.col] = None
            move: Move = Move(old_posn=old_posn, new_posn=new_posn, piece=piece)
            self.moves.append(move)
            return True
        return False

    def __str__(self) -> str:
        return "\n".join("".join(str(piece or ' ') for piece in row) for row in self.board)


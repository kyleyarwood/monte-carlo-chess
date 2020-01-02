from monte_carlo_chess import config
from .posn import Posn


def is_on_board(posn: Posn):
    if 0 <= posn.row < config.BOARD_SIZE and 0 <= posn.col < config.BOARD_SIZE:
        return True
    return False


def same_colour_in_spot(posn, board, colour):
    return board[posn] is not None and board[posn].colour == colour


# sqaures between but not including curr_posn and new_posn
def path(
    curr_posn: Posn,
    new_posn: Posn,
    board: board,
    can_be_straight: bool = True,
    can_be_diagonal: bool = True,
):
    if not can_be_straight and not can_be_diagonal:
        raise ValueError("Path cant be vaild and be not straight and not diagonal")

    if not is_on_board(curr_posn):
        raise IndexError(
            f"Board has size {config.BOARD_SIZE}. curr_posn is not chessBoard"
        )

    if not is_on_board(new_posn):
        raise IndexError(
            f"Board has size {config.BOARD_SIZE}. new_posn is not chessBoard"
        )

    if curr_posn == new_posn:
        raise ValueError("curr_posn can't equal new_posn")

    if (
        curr_posn[0] != new_posn[0]
        and curr_posn[1] != new_posn[1]
        and abs(curr_posn[0] - new_posn[0]) != abs(curr_posn[1] - new_posn[1])
    ):
        raise ValueError("Path is invaild (not diagonal or straight)")

    if not can_be_straight and (
        curr_posn[0] == new_posn[0] or curr_posn[1] == new_posn[1]
    ):
        raise ValueError("can_be_straight is false and path is straight")

    if (
        not can_be_diagonal
        and curr_posn[0] != new_posn[0]
        and curr_posn[1] != new_posn[1]
    ):
        raise ValueError("can_be_diagonal is False and path is diagonal")

    slope = []
    for c, n in zip(curr_posn, new_posn):
        slope.append(0 if not (n - c) else (n - c) // abs(n - c))

    curr_posn[0] += slope[0]
    curr_posn[1] += slope[1]
    while curr_posn != new_posn:
        yield board[curr_posn]
        curr_posn[0] += slope[0]
        curr_posn[1] += slope[1]

def clear_path(curr_posn: Posn, new_posn: Posn, board: board, piece_colour):
    return all(
        map(lambda x: x is None, path(curr_posn, new_posn, board))
    ) and not same_colour_in_spot(new_posn, board, piece_colour)

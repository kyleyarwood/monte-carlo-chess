from monte_carlo_chess import config


def validate_posn(posn):
    if not hasattr(posn, '__len__'):
        raise TypeError("posn must have a length")
    elif not hasattr(posn, "__getitem__"):
        raise TypeError("posn must have __getitem__")
    elif len(posn) != 2:
        raise ValueError("posn must have length 2")
    elif not isinstance(posn[0], int) or not isinstance(posn[1], int):
        raise ValueError("posn values must be an int")
    elif posn[0] not in range(config.BOARD_SIZE) or posn[1] not in range(
            config.BOARD_SIZE):
        raise IndexError("posn values must be between 0 and " +
                         str(config.BOARD_SIZE) + "(BOARD_SIZE-1) (inclusive)")
    return True


def is_on_board(posn):
    if validate_posn(posn):
        if posn[0] in range(config.BOARD_SIZE) and posn[1] in range(config.BOARD_SIZE):
            return True
        else:
            return False

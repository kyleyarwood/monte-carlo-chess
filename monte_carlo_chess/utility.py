from monte_carlo_chess import config


def vaild_posin(posin):
    if not hasattr(posin, '__len__'):
        raise TypeError("posin must have a length")
    elif not hasattr(posin, "__getitem__"):
        raise TypeError("posin must have __getitem__")
    elif len(posin) != 2:
        raise ValueError("posin must have length 2")
    elif not isinstance(posin[0], int) or not isinstance(posin[1], int):
        raise ValueError("posin values must be an int")
    elif posin[0] not in range(config.BOARD_SIZE) or posin[1] not in range(
            config.BOARD_SIZE):
        raise IndexError("posin values must be between 0 and " +
                         str(config.BOARD_SIZE) + "(BOARD_SIZE-1) (inclusive)")
    return True

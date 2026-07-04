from models.vector import Vector

class Posn:
    def __init__(self, *, row: int, col: int):
        self.row = row
        self.col = col

    def __add__(self, vector: Vector) -> 'Posn':
        if isinstance(vector, Vector):
            return Posn(row=self.row + vector.dx, col=self.col + vector.dy)
        raise NotImplementedError(f"Can't add Posn with {type(vector)}")

    def __eq__(self, other: 'Posn') -> bool:
        if not isinstance(other, Posn):
            return False
        return self.row == other.row and self.col == other.col

    __radd__ = __add__


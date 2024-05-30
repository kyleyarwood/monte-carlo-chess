from models.vector import Vector

class Posn:
    def __init__(self, *, row: int, col: int):
        self.row = row
        self.col = col

    def __add__(self, vector: Vector) -> 'Posn':
        if isinstance(vector, Vector):
            return Posn(row=self.row + vector.dx, col=self.col + vector.dy)
        raise NotImplementedError(f"Can't add Posn with {type(vector)}")

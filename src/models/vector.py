class Vector:
    def __init__(self, *, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def __mul__(self, factor) -> 'Vector':
        if isinstance(factor, int):
            return Vector(dx=self.dx*factor, dy=self.dy*factor)
        raise NotImplementedError(f"Can't multiply vector by non-integer type: {factor}")

    __rmul__ = __mul__


import pytest
from models.vector import Vector
from models.posn import Posn

def test_add_posn_and_vector():
    pos = Posn(row=1, col=2)
    vec = Vector(dx=3, dy=4)
    result = pos + vec
    assert result.row == 4
    assert result.col == 6

def test_add_posn_and_non_vector():
    pos = Posn(row=1, col=2)
    with pytest.raises(NotImplementedError):
        pos + "invalid_type"

def test_add_posn_and_none():
    pos = Posn(row=1, col=2)
    with pytest.raises(NotImplementedError):
        pos + None

if __name__ == "__main__":
    pytest.main()


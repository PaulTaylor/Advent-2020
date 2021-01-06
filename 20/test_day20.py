import pytest, os
from day20 import *

@pytest.fixture
def test_input():
    with open(os.path.dirname(__file__) + '/test_input.txt', 'r') as f:
        return f.read()

def test_part_a(test_input):
    tiles = create_tiles(test_input)
    assert len(tiles) == 9
    assert part_a(tiles) == 20899048083289
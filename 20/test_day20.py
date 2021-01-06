import pytest, os
from day20 import *

@pytest.fixture
def tiles():
    with open(os.path.dirname(__file__) + '/test_input.txt', 'r') as f:
        raw = f.read()
        return create_tiles(raw)

def test_parts_ab(tiles):
    a_ans, sub_G = do_part_a(tiles)
    assert a_ans == 20899048083289

    assert do_part_b(tiles, sub_G) == 273
import pytest, os
from day20 import *

@pytest.fixture
def tiles():
    with open(os.path.dirname(__file__) + '/test_input.txt', 'r') as f:
        raw = f.read()
        return create_tiles(raw)

@pytest.fixture
def edge_lookup(tiles):
    return create_edge_lookup(tiles)

def test_get_tile_edges():
    arr = np.array([["A", "B", "C"], ["D", "E", "F"], ["H", "I", "J"]])
    assert arr.shape == (3,3)

    assert get_tile_edges(arr) == ("ABC", "ADH", "CFJ", "HIJ")

def test_create_edge_lookup(tiles, edge_lookup):
    lkp = edge_lookup
    assert "top_2311_r0" in lkp["..##.#..#."]
    assert "bottom_1427_r0" in lkp["..##.#..#."]
    assert len(lkp["..##.#..#."]) == 4

def test_part_a(tiles, edge_lookup):
    grid = fit_into_grid(tiles, edge_lookup)
    assert part_a(grid) == 20899048083289
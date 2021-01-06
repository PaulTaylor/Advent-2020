"Clean implementation of day 20"

import networkx as nx
import numpy as np
import sys

from collections import defaultdict, deque
from math import sqrt

def create_tiles(raw):
    tiles = {}
    current = []
    current_id = None

    for line in raw.splitlines():
        if "Tile " in line:
            current_id = line[(line.index(" ") + 1):-1]
        elif len(line.strip()) == 0:
            # gap, prep for next tile
            tiles[current_id] = np.array(current, ndmin=2)
            current = []
            current_id = None
        else:
            # line in a tile
            current.append(list(line))

    tiles[current_id] = np.array(current)

    return tiles

def get_tile_edges(tile):
    ":returns: top, left, right, bottom"
    return "".join(tile[0]), \
           "".join(tile[:, 0]), \
           "".join(tile[:, -1]), \
           "".join(tile[-1])

def create_edge_lookup(tiles):
    lookup = defaultdict(set)
    for rot in range(4):
        for tid, tile in tiles.items():
            top, left, right, bottom = get_tile_edges(np.rot90(tile, rot))
            lookup[top].add(f"top_{tid}_r{rot}")
            lookup[left].add(f"left_{tid}_r{rot}")
            lookup[right].add(f"right_{tid}_r{rot}")
            lookup[bottom].add(f"bottom_{tid}_r{rot}")

    # Lets scan these to remove edges that are self-referencing (have only 1 tid in them)
    for k, v in list(lookup.items()):
        tids = { x.split("_")[1] for x in v }
        if len(tids) < 2:
            del lookup[k]

    return lookup
  
def find_top_left(edge_lookup):
    # In edge_lookup the top left corner will only have bottom and right
    # edges appearing in the lookup
    temp = defaultdict(set)
    for v in edge_lookup.values():
        for i in v:
            direction, tid, r = i.split("_")
            temp[tid + r].add(direction)
    
    candidates = [ tid_r for tid_r, edge_set in temp.items() if edge_set == { "bottom", "right" } ]
    return sorted(candidates, key=lambda x: int(x[-1]))

def fit_into_grid(tiles, edge_lookup):
    "Need to identify the corners and multiple the tile ids together"
    final_grid_size = int(sqrt(len(tiles)))

    # Get the top left corner
    tl_candidates = find_top_left(edge_lookup)

    # Now find the tiles that fit below it
    print(tl_candidates)
    for tl_cand in tl_candidates:
        try:
            last_tid, last_rot = tl_cand.split("r")
            grid = [[(last_tid, last_rot)]]
            for _ in range(1, final_grid_size):
                _, _, _, lt_bottom_edge = get_tile_edges(np.rot90(tiles[last_tid], int(last_rot)))
                next_cands = [ x for x in edge_lookup[lt_bottom_edge] if "top" in x ]
                if not next_cands:
                    # Need to try flips - so we check if there's a "bottom" match
                    next_cands = [ x for x in edge_lookup[lt_bottom_edge] if "top" in x and last_tid not in x ]
                    assert len(next_cands) == 1, f"Multiple choice in flip step!\n{next_cands}"
                    # XXX is this rot still appropriate if we've flipped the tile?
                    last_tid, last_rot = next_cands[0].split("_")[1:]
                    tiles[last_tid] = np.flipud(tiles[last_tid])

                assert len(next_cands) == 1, f"Multiple choice of top left tile!\n{next_cands} in {grid}"
                last_tid, last_rot = next_cands[0].split("_")[1:]
                last_rot = last_rot[-1]
                grid.append([(last_tid, last_rot)])
            break
        except AssertionError:
            pass
    
    assert len(grid) == final_grid_size
    del lt_bottom_edge, next_cands, last_tid, last_rot

    # Now we have the first column all complete - run through each row to extend it left->right
    for row in grid:
        last_tid, last_rot = row[0]
        for _ in range(1, final_grid_size):
            _, _, lt_right_edge, _ = get_tile_edges(np.rot90(tiles[last_tid], int(last_rot)))
            next_cands = [ x for x in edge_lookup[lt_right_edge] if "left" in x ]
            if not next_cands:
                # Need to try flips - so we check if there's a "right" match
                next_cands = [ x for x in edge_lookup[lt_right_edge] if "right" in x and last_tid not in x ]
                assert len(next_cands) == 1, f"Multiple choice in flip step!\n{next_cands}"
                # XXX is this rot still appropriate if we've flipped the tile?
                last_tid, last_rot = next_cands[0].split("_")[1:]
                tiles[last_tid] = np.fliplr(tiles[last_tid])

            assert len(next_cands) == 1, f"Multiple choice!\n{next_cands}"
            
            last_tid, last_rot = next_cands[0].split("_")[1:]
            last_rot = last_rot[-1]
            row.append((last_tid, last_rot))

    return grid

def part_a(grid):
    return int(grid[0][0][0]) * int(grid[-1][0][0]) * int(grid[0][-1][0]) * int(grid[-1][-1][0])

if __name__ == "__main__":
    with open(sys.argv[-1], "r") as f:
        raw = f.read()
        tiles = create_tiles(raw)
    
    edge_lookup = create_edge_lookup(tiles)
    grid = fit_into_grid(tiles, edge_lookup)
    print("Part A = ", part_a(grid))
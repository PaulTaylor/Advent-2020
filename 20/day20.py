import numpy as np
import networkx as nx
import math, sys

from collections import defaultdict
from itertools import product
from pprint import pprint

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

def part_a(tiles):
    edges = {}
    match_counts = defaultdict(set)
    for id, tile in tiles.items():
        print(tile.shape)
        edges[id] = [
            "".join(tile[0]),    # top
            "".join(tile[:, 0]), # left edge
            "".join(tile[:, -1]),# right edge
            "".join(tile[-1])    # bottom
        ]

        for r in range(1, 4):
            rot = np.rot90(tile, r)
            edges[id].extend([
                "".join(rot[0]),    # top
                "".join(rot[:, 0]), # left edge
                "".join(rot[:, -1]),# right edge
                "".join(rot[-1])    # bottom
            ])

        assert len(edges[id]) == 16

    for tile_id, edge_list in edges.items():
        for other_tile_id, other_edge_list in edges.items():
            if tile_id == other_tile_id:
                continue

            combinations = product(edge_list, other_edge_list)
            for e1, e2 in combinations:
                if e1 == e2:
                    match_counts[tile_id].add(other_tile_id)

    pprint(match_counts)

    G = nx.Graph()
    for src, others in match_counts.items():
        for o in others:
            G.add_edge(src, o)

    nx.nx_agraph.write_dot(G, "the-graph.dot")

    acc = 1
    for n in G.nodes():
        degree = G.degree(n)
        if degree == 2: # corners only have 2 links :)
            acc *= int(n)
        
    return acc

if __name__ == "__main__":
    raw = sys.stdin.read()
    tiles = create_tiles(raw)
    print(part_a(tiles))
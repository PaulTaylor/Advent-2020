import numpy as np

from day23 import *

def check_equal(actual, desired):
    a_actual = np.array(actual)
    a_desired = np.array(desired)

    # roll desired so that it looks like actual
    idx, = np.where(a_desired == a_actual[0])[0]
    a_desired = np.roll(a_desired, -idx)

    return np.array_equal(a_actual, a_desired)

def test_part_a():
    cups = np.array([ int(x) for x in "389125467" ])
    current = cups[0]
    
    # Round 1
    cups, current = do_round(cups, current)
    # Verify the start of R2 state
    assert check_equal(cups, [3,2,8,9,1,5,4,6,7])
    assert current == 2
    cups, current = do_round(cups, current) 
    # Start of R3
    assert check_equal(cups, [3,2,5,4,6,7,8,9,1])
    assert current == 5
    cups, current = do_round(cups, current)
    # Start of R4
    assert check_equal(cups, [7,2,5,8,9,1,3,4,6])
    assert current == 8
    cups, current = do_round(cups, current)
    # Start of R5
    assert check_equal(cups, [3,2,5,8,4,6,7,9,1]), "SR5"
    assert current == 4
    cups, current = do_round(cups, current)
    # Start of R6
    assert check_equal(cups, [9,2,5,8,4,1,3,6,7]), "SR6"
    assert current == 1
    cups, current = do_round(cups, current)
    # Start of R7
    assert check_equal(cups, [7,2,5,8,4,1,9,3,6]), "SR7"
    assert current == 9
    cups, current = do_round(cups, current)
    # Start of R8
    assert check_equal(cups, [8,3,6,7,4,1,9,2,5]), "SR8"
    assert current == 2
    cups, current = do_round(cups, current)
    # Start of R9
    assert check_equal(cups, [7,4,1,5,8,3,9,2,6]), "SR9"
    assert current == 6
    cups, current = do_round(cups, current)
    # Start of R10
    assert check_equal(cups, [5,7,4,1,8,3,9,2,6]), "SR10"
    assert current == 5
    cups, current = do_round(cups, current)

    assert "92658374" == create_string(cups)

    for _ in range(90):
        cups, current = do_round(cups, current)

    assert create_string(cups) == "67384529"
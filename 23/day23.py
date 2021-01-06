import numpy as np
import sys

from numba import njit
from tqdm import tqdm

@njit
def generate_dest_label(cl, lowest_cup, highest_cup):
    dl = cl - 1
    if dl < lowest_cup:
        return highest_cup
    else:
        return dl

@njit
def do_round(cups, current_label):
    current_index, = np.where(cups == current_label)[0]
    lowest_cup = min(cups)
    highest_cup = max(cups)

    # Make sure current cup is at position 0 before this method is called
    cups = np.roll(cups, -current_index)

    # remove 3 cups immediately to the right of the current cup
    removed = np.copy(cups[1:4])
    cups[1:4] = -1
    cups[1:] = np.roll(cups[1:], -3)

    # Calculate destination
    destination_label = generate_dest_label(current_label, lowest_cup, highest_cup)
    while destination_label in removed:
        destination_label = generate_dest_label(destination_label, lowest_cup, highest_cup)

    #print("Destination label: ", destination_label)
    destination_index, = np.where(cups == destination_label)[0]

    # Add back the removed cups after the destination index
    cups[destination_index + 1:] = np.roll(cups[destination_index + 1:], 3)
    cups[destination_index+1:destination_index+4] = removed
    #print("rv = ", cups)
    
    # Calculate the new "current" value and return
    return cups, cups[1]

def create_string(cups):
    idx_of_one, = np.where(cups == 1)[0]
    cups = [ str(x) for x in cups ]
    return "".join(cups[idx_of_one + 1:]) + "".join(cups[0:idx_of_one])

if __name__ == "__main__":
    cups = np.array([ int(x) for x in "739862541" ])
    current = cups[0]
    for _ in range(100):
        cups, current = do_round(cups, current)

    ans = create_string(cups)
    assert ans != "76345298", "Incorrect answer"
    print(ans)

    # Part B
    cups = [ int(x) for x in "739862541" ]
    current = cups[0]

    num = max(cups) + 1
    while len(cups) < 1e6:
        cups.append(num)
        num += 1
    cups = np.array(cups)

    for _ in tqdm(range(10000000)):
        cups, current = do_round(cups, current)

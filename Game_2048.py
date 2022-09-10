"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

LOST1 = False
LOST2 = False

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code

    dummy_line = list(line)
    leng = len(dummy_line)
    loop_lapse = 0
    parallel_list = []
    bag_last = False
    last_two = False

    # remove all zeros

    iter_ind = dummy_line.count(0)

    while iter_ind > 0:
        dummy_line.remove(0)
        iter_ind -= 1

    leng_1 = len(dummy_line)

    # return dummy_line if leng_1 == 1
    if leng_1 == 1:
        if leng_1 != leng:
            diff = leng - leng_1
            while diff > 0:
                dummy_line.append(0)
                diff -= 1
        return dummy_line

    for ind in range(leng_1 - 1):

        if loop_lapse > 0:
            loop_lapse -= 1
            continue

        a_ele = dummy_line[ind]

        j_ind = ind + 1

        b_ele = dummy_line[j_ind]

        if a_ele == b_ele:
            if ind == leng_1 - 3:
                bag_last = True

            parallel_list.append(a_ele * 2)
            loop_lapse += 1
        else:
            parallel_list.append(a_ele)
            if ind == leng_1 - 2:
                last_two = True

    if bag_last or last_two:
        bag_last = False
        last_two = False
        parallel_list.append(dummy_line[-1])

    leng_2 = len(parallel_list)

    if leng_2 < leng:
        diff = leng - leng_2
        while diff > 0:
            parallel_list.append(0)
            diff -= 1


    return parallel_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.height = grid_height
        self.width = grid_width

        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self.grid = list()
        for ind_i in range(self.height):
            dummy = []
            for ind_j in range(self.width):
                dummy.append(0)
            self.grid.append(dummy)

        for ind_k in range(2):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        string1 = 'This is a {} x {} grid!'.format(self.height, self.width)
        print(string1)
        for ind_i in range(self.height):
            print('')
            for ind_j in range(self.width):
                print(self.grid[ind_i][ind_j], end = '\t')
        return ''

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        # code for UP and LEFT as DOWN is reverse of UP etc.
        changed = False
        rev = False
        if direction in [DOWN, RIGHT]:
            rev = True

        if direction in [UP, DOWN]:
            for col_ind in range(self.width):
                dummy = []
                for row_ind in range(self.height):
                    dummy.append(self.grid[row_ind][col_ind])

                if rev:
                    dummy.reverse()
                merged_dummy = merge(dummy)
                if rev:
                    merged_dummy.reverse()

                if merged_dummy != dummy:
                    changed = True

                for row_ind in range(self.height):
                    self.grid[row_ind][col_ind] = merged_dummy[row_ind]

        if direction in [LEFT, RIGHT]:
            for row_ind in range(self.height):
                dummy = []
                for col_ind in range(self.width):
                    dummy.append(self.grid[row_ind][col_ind])

                if rev:
                    dummy.reverse()
                merged_dummy = merge(dummy)
                if rev:
                    merged_dummy.reverse()

                if merged_dummy != dummy:
                    changed = True

                for col_ind in range(self.width):
                    self.grid[row_ind][col_ind] = merged_dummy[col_ind]

        if changed:
            self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        select_from = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        empty_tile = False
        done_set = set([])

        while not empty_tile:
            ind_i = random.randrange(self.height)
            ind_j = random.randrange(self.width)

            done_set.add((ind_i, ind_j))
            if len(done_set) == self.height * self.width:
                return

            if self.grid[ind_i][ind_j] == 0:
                empty_tile = True

        random.shuffle(select_from)
        self.grid[ind_i][ind_j] = select_from[0]

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self.grid[row][col]

Game = TwentyFortyEight(4, 4)
poc_2048_gui.run_gui(Game)
print(Game)

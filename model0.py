"""Model for Slide game - keeps data in a double array, such that Model[x][y]
refers to the value at (x,y) on the grid displayed to the user."""
import random
import slideexceptions
from Observable import Observable


class Model:

    size = None
    game_states = {"Win": "you win!", "Loss": "you lose!", "Play": 0}
    unoccupied_squares = None
    game_goal = 2048
    empty_square_value = 0
    new_block_value = 2

    def __init__(self, num):
        """
            Initilizes the model to represent a start board -
            A board of the given size with only one randomly placed block of value 2
            Will throw TypeError if num is not an integer greater than or equal to 2
        """
        if num < 2:
            raise TypeError('Arugment number must be larger than 2')
        self.size = int(num)
        self.unoccupied_squares = []
        l = []
        # build the grid of empty squares, and add all to the list of unoccupied squares
        for i in range(num):
            m = []
            for j in range(num):
                coordinate = i, j
                self.unoccupied_squares.append(coordinate)
                m.append(self.empty_square_value)
            l.append(m)
        # the grid is observable, so the controller can listen for changes
        self.grid = l
        self.last_move = Observable(None)
        self.add_new_block()

    def add_block_at(self, x, y, value):
        """
            Adds a block at a specific point on the board
            Overwrites any value that is at the coordinate defined by (x,y)
            Does not check to see if coordinate is valid before adding
        """
        self.grid[x][y] = value
        if (x, y) in self.unoccupied_squares and value != self.empty_square_value:
            self.unoccupied_squares.remove((x, y))
        elif value == self.empty_square_value:
            self.unoccupied_squares.append((x, y))

    def add_new_block(self):
        """
            Adds a new block to a random non-occupied (value of zero) square on the board
            Returns the coordinates of the addition as a tuple
        """
        if len(self.unoccupied_squares) == 0:
            raise slideexceptions.AddBlockError("GameBoard is Full")
        new_x, new_y = self.unoccupied_squares.pop(int(random.random() * len(self.unoccupied_squares)))
        self.grid[new_x][new_y] = self.new_block_value
        return (new_x, new_y)

    def value_at(self, x, y):
        """
            Gets the value of the grid at the coordinate (x,y) on the board.
            Arugments:
                x (int) - x coordinate
                y (int) - y coordinate
        """
        return self.grid[x][y]

    def count_blocks(self):
        """
            Counts the number of blocks on the board
            Returns an integer representing the number of blocks on the board
        """
        result = 0
        for i in range(self.size):
            for j in range(self.size):
                b = self.value_at(i, j)
                if b > self.empty_square_value:
                    result += 1
        return result

    def shift_blocks_left(self):
        """
            Shifts all blocks left and collapses same-valued blocks into their left neighbor
        """
        return self._shift_blocks(1, 1)

    def shift_blocks_right(self):
        """
            Shifts all blocks right and collapses same-valued blocks
        """
        return self._shift_blocks(1, 0)

    def shift_blocks_up(self):
        """
            Shifts all blocks up and collapses same-valued blocks
        """
        return self._shift_blocks(0, 1)

    def shift_blocks_down(self):
        """
            Shifts all blocks down and collapses same-valued blocks
        """
        return self._shift_blocks(0, 0)

    def _shift_blocks(self, shift_horizontal, shift_to_bottom_left):
        """
            Abstraction for shifting blocks in a direction
            Takes two arguements:
            shift_horizontal: Boolean - True means movement left-right, False means up-down
            shift_to_bottom_left: Boolean - True means movement toward origin(down,left), false means away(up,right)
            this means that the four direction have the following arguments:
            Left:  self._shift_blocks(1,1)
            Right: self._shift_blocks(1,0)
            Up:    self._shift_blocks(0,0)
            Down:  self._shift_blocks(0,1)
            returns True if no blocks have moved positions, otherwise returns false
        """
        no_merged = True
        no_moves = 0
        for outer_iteration_value in range(self.size):
            last_block_val = self.empty_square_value
            # initialize the last open grid square to be the first square that will be checked, which is the lowest
            # number on the axis if moving down or left, otherwise it is the highest
            if shift_to_bottom_left:
                last_open = 0
            else:
                last_open = self.size - 1
            for inner_iteration_value in range(self.size):
                # if the blocks are being shifted down or left, the algorithm should look for blocks
                # with a lower coordinate value on the axis of movement (Y and X respectively), and should
                # begin its search from the lowest value of the axis of non movement (X and Y respectively)
                # if the blocks are being shfited up or right, the opposite is true
                if shift_to_bottom_left:
                    directional_adjustment = -1
                else:
                    inner_iteration_value = self.size - inner_iteration_value - 1
                    directional_adjustment = 1
                # if the blocks are being shifted horizontailly, iterate first by y coord, then x coord, i.e.
                # check spot (0,0), then (0,1), then (0,2). Otherwise, do the reverse
                if shift_horizontal:
                    x_coord_old = inner_iteration_value
                    y_coord_old = outer_iteration_value
                else:
                    x_coord_old = outer_iteration_value
                    y_coord_old = inner_iteration_value
                val = self.grid[x_coord_old][y_coord_old]
                # Check for case where blocks could merge
                if val > self.empty_square_value and val == last_block_val:
                    last_block_val = val + val
                    m = self._block_merge(last_block_val, x_coord_old, y_coord_old, last_open,
                                          directional_adjustment, shift_horizontal, shift_to_bottom_left)
                    self.last_move.set(m)
                    no_merged = False
                # Check for case where block could slide and collide
                elif val > self.empty_square_value:
                    m = self._block_collide(val, x_coord_old, y_coord_old, last_open,
                                            shift_horizontal, shift_to_bottom_left)
                    last_block_val = val
                    last_open = last_open + (0 - directional_adjustment)
                    if m[0] != m[1]:
                        self.last_move.set(m)
                    else:
                        no_moves += 1
        return no_moves == self.count_blocks() and no_merged

    def _block_merge(self, new_val, x_coord_old, y_coord_old, last_open, directional_adjustment,
                     shift_horizontal, shift_to_bottom_left):
        """
            Handles blocks of same value colliding with eachother and becoming a single block of twice
            their value
            Returns a tuple of coordinates - (old coordinates, new coordinates)
        """
        if shift_horizontal:
            x_coord_new = last_open + directional_adjustment
            y_coord_new = y_coord_old
        else:
            x_coord_new = x_coord_old
            y_coord_new = last_open + directional_adjustment
        self.grid[x_coord_new][y_coord_new] = new_val
        self.grid[x_coord_old][y_coord_old] = self.empty_square_value
        self.unoccupied_squares.append((x_coord_old, y_coord_old))
        old_coords = (x_coord_old, y_coord_old)
        new_coords = (x_coord_new, y_coord_new)
        return (old_coords, new_coords)

    def _block_collide(self, new_val, x_coord_old, y_coord_old, last_open, shift_horizontal,
                       shift_to_bottom_left):
        """
            Handles blocks moving and colliding with their right-most obstacle
            (wall or block of different value)
            Returns a tuple of coordinates - (old coordinates, new coordinates)
        """
        if shift_horizontal:
            x_coord_new = last_open
            y_coord_new = y_coord_old
        else:
            x_coord_new = x_coord_old
            y_coord_new = last_open
        self.grid[x_coord_old][y_coord_old] = 0
        self.grid[x_coord_new][y_coord_new] = new_val
        self.unoccupied_squares.append((x_coord_old, y_coord_old))
        self.unoccupied_squares.remove((x_coord_new, y_coord_new))
        old_coords = (x_coord_old, y_coord_old)
        new_coords = (x_coord_new, y_coord_new)
        return (old_coords, new_coords)

    def game_state_check(self):
        """
            Returns the state of the game, which is one of the three values in the game_states
            class dictionary
        """
        column_maxes = []
        for column in self.grid:
            column_maxes.append(max(column))
        board_max = max(column_maxes)
        if board_max == self.game_goal:
            return self.game_states["Win"]
        if self.no_valid_moves():
            return self.game_states["Loss"]
        return self.game_states["Play"]

    def no_valid_moves(self):
        """
            Determine if there are any valid moves available
            Returns a boolean - True if any of the four moves are possible
        """
        if self.count_blocks() == (self.size * self.size):
            #The board is full of blocks, now check if any could be merged
            for i in range(self.size):
                for j in range(self.size):
                    val = self.grid[i][j]
                    left = (i > 0) and (self.grid[i - 1][j] == val)
                    right = (i < self.size - 1) and (self.grid[i + 1][j] == val)
                    down = (j > 0) and (self.grid[i][j - 1] == val)
                    up = (j < self.size - 1) and (self.grid[i][j + 1] == val)
                    if left or right or down or up:
                        #Theres a direction that you can move in!
                        return False
            # Theres no direction you can move in!
            return True
        # Board is not full, so obviously there is a spot a block could slide into
        return False

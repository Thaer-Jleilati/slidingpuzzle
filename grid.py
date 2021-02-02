import random

all_grids_used_in_solve = set()

class Grid:
    def __init__(self, w = 3, h = 3, copy_grid = None, iterdepth = 0):
        self.solved = False
        self.iterdepth = iterdepth

        if copy_grid is None:        
            self.WIDTH = w
            self.HEIGHT = h
        
            self.all_positions = None

            self.initiate_tiles() # Initiate the grid in an ordered way
            self.shuffle_tiles()
        else:
            self.WIDTH = copy_grid.WIDTH
            self.HEIGHT = copy_grid.HEIGHT
            self.solved = False
            self.all_positions = [pos for pos in copy_grid.all_positions]        
        
    def initiate_tiles(self):
        self.all_positions = [(j, i) for i in range(self.HEIGHT) for j in range(self.WIDTH)]
        self.solved = True

    def shuffle_tiles(self):
        random.shuffle(self.all_positions)

        for (i, pos) in enumerate(self.all_positions):        
            if (pos is not None and pos[0] == self.WIDTH-1 and pos[1] == self.HEIGHT-1):
                self.all_positions[i] = None # Put back blank tile - used after we shuffle again after we solve it
        self.solved = False
        print(self.all_positions)

    def convert_linear_idx(self, tile_x, tile_y):
        return tile_y * self.WIDTH + tile_x

    def get_tile_position(self, tile_x, tile_y):
        return self.all_positions[self.convert_linear_idx(tile_x, tile_y)]

    def swap(self, tile_x_1, tile_y_1, tile_x_2, tile_y_2):
        tile1 = self.get_tile_position(tile_x_1, tile_y_1)
        tile2 = self.get_tile_position(tile_x_2, tile_y_2)
        self.all_positions[self.convert_linear_idx(tile_x_1, tile_y_1)] = tile2
        self.all_positions[self.convert_linear_idx(tile_x_2, tile_y_2)] = tile1

    def check_solve(self):
        ordered_positions = [(j, i) for i in range(self.HEIGHT) for j in range(self.WIDTH)]
        #No need to check the last tile cuz thats blank
        if (ordered_positions[:-1] == self.all_positions[:-1]):
            self.all_positions[-1] = (self.WIDTH-1, self.HEIGHT-1) # Remove blank tile
            self.solved = True
        return self.solved

    def click_on_tile(self, tile_x, tile_y):
        # check if adjacent to blank
        adjacent_idxs = [(-1, 0), (0, -1), (0, +1), (1, 0)]
        for d_x, d_y in adjacent_idxs:
            a_x, a_y = tile_x + d_x, tile_y + d_y
            if a_x < 0 or a_x >= self.WIDTH or a_y < 0 or a_y >= self.HEIGHT:
                continue # Index out of bounds, don't check that tile
            adjacent_tile = self.get_tile_position(a_x, a_y)

            # We found the blank tile, now swap them
            if adjacent_tile is None:
                #print(f"Swapping tile at {tile_x},{tile_y} with blank at {a_x},{a_y}")
                self.swap(tile_x, tile_y, a_x, a_y)
                return True # succesful click
        return False

    #
    #1: we get the location of the blank tile
    #2: if it's in the middle = 4 moves, if it's in corner = 2 moves, if it's on sides = 3 moves
    #3 try those moves?

    def check_valid_moves(self):
        moves = []

        idx = self.all_positions.index(None)
        tile_x = idx % self.WIDTH
        tile_y = idx // self.WIDTH
        adjacent_idxs = [(tile_x -1, tile_y + 0), (tile_x + 0, tile_y -1), (tile_x + 0, tile_y + 1), (tile_x + 1, tile_y + 0)]
        for a_x, a_y in adjacent_idxs:
            if a_x < 0 or a_x >= self.WIDTH or a_y < 0 or a_y >= self.HEIGHT:
                continue # Index out of bounds, don't check that tile
            moves.append((a_x, a_y))

       #print(moves)
        return moves

    #[(1, 0), None, (2, 1), (1, 3), (2, 0), (0, 2), (0, 0), (0, 1), (2, 2), (1, 2), (1, 1), (0, 3)]
    def solve(self):
        print("Calling solve on grid with ITERDETPHHHHHHHH "  + str(self.iterdepth) )
        valid_moves = self.check_valid_moves()
        for move in valid_moves:
            new_grid = Grid(copy_grid = self, iterdepth=(self.iterdepth + 1))
            stringed_list = str(new_grid.all_positions)
            if stringed_list not in all_grids_used_in_solve:
                print("MOVING " + str(move))
                new_grid.click_on_tile(*move)

                all_grids_used_in_solve.add(stringed_list)

                if (new_grid.check_solve()):
                    print("SOLVED!")
                    print(new_grid)
                    return True

                new_grid.solve()
            else:
                print("Found this grid " + str(self.all_positions) + " already, skipping")
                continue # Grid has been seen before, move on to next branch



            #basicaly we need a hash or some data structue from which we can load a specific grid
            #every time we call the move method, we save a copy of the grid's hash
            #this means we can go 'up' the tree
            # so basically we go deep until we reach a point where the grid == a grid we've seen before (we compare hash)
            # then we goback up the tree and into another branch?

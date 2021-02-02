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
            self.moves_so_far = []

            self.initiate_tiles() # Initiate the grid in an ordered way
            self.shuffle_tiles()
        else:
            self.WIDTH = copy_grid.WIDTH
            self.HEIGHT = copy_grid.HEIGHT
            self.solved = False
            self.moves_so_far = copy_grid.moves_so_far[:] # create a copy
            self.all_positions = copy_grid.all_positions[:] # create a copy
        
    def initiate_tiles(self):
        self.all_positions = [(j, i) for i in range(self.HEIGHT) for j in range(self.WIDTH)]
        self.moves_so_far.clear()
        self.solved = True

    def shuffle_tiles(self):
        # Put in blank tile if it doesn't exist yet.
        for (i, pos) in enumerate(self.all_positions):        
            if (pos is not None and pos[0] == self.WIDTH-1 and pos[1] == self.HEIGHT-1):
                self.all_positions[i] = None 

        # Play 100 random moves
        for i in range(100):
            valid_moves = Grid.check_valid_moves(self)
            move = random.choice(valid_moves)
            self.click_on_tile(*move)

        self.solved = False
        self.moves_so_far.clear()

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
                self.moves_so_far.append((tile_x, tile_y))
                #print(f"Swapping tile at {tile_x},{tile_y} with blank at {a_x},{a_y}")
                self.swap(tile_x, tile_y, a_x, a_y)
                return True # succesful click
        return False

    #
    #1: we get the location of the blank tile
    #2: if it's in the middle = 4 moves, if it's in corner = 2 moves, if it's on sides = 3 moves
    #3 try those moves?

    def check_valid_moves(grid):
        moves = []

        idx = grid.all_positions.index(None)
        tile_x = idx % grid.WIDTH
        tile_y = idx // grid.WIDTH
        adjacent_idxs = [(tile_x -1, tile_y + 0), (tile_x + 0, tile_y -1), (tile_x + 0, tile_y + 1), (tile_x + 1, tile_y + 0)]
        for a_x, a_y in adjacent_idxs:
            if a_x < 0 or a_x >= grid.WIDTH or a_y < 0 or a_y >= grid.HEIGHT:
                continue # Index out of bounds, don't check that tile
            moves.append((a_x, a_y))

        return moves

    def get_child_grids_to_solve(grid):
        valid_moves = Grid.check_valid_moves(grid)
        child_grids = []
        for move in valid_moves:
            #print("Attempting " + str(grid.iterdepth) + " MOVING " + str(move))
            new_grid = Grid(copy_grid = grid, iterdepth=(grid.iterdepth + 1))
            new_grid.click_on_tile(*move)
            
            hashed = str(new_grid.all_positions)
            if hashed in all_grids_used_in_solve:
                #print("Found this grid " + str(new_grid.all_positions) + " already, skipping")
                continue
            else:
                all_grids_used_in_solve.add(hashed)
                child_grids.append(new_grid)
        return child_grids

    def solve(self):
        all_grids_used_in_solve.clear()
        self.moves_so_far.clear()
        next_grids_to_solve = Grid.get_child_grids_to_solve(self)
        for child_grid in next_grids_to_solve:
            if child_grid.check_solve():
                print(f"SOLVED! in {child_grid.iterdepth} moves: ", child_grid.moves_so_far)
                all_grids_used_in_solve.clear()
                return child_grid.moves_so_far
            next_grids_to_solve.extend(Grid.get_child_grids_to_solve(child_grid))
        print("No solves found. Number grids attempted: " + str(len(all_grids_used_in_solve))) 
        all_grids_used_in_solve.clear()
        return None           
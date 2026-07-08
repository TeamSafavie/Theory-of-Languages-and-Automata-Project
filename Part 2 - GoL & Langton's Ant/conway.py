"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""
import numpy as np
from scipy import signal, ndimage


def parse_pattern(filepath):
    """
    TODO: [Part 1d - RLE/Plaintext Parser]
    Write a parser for Run Length Encoded (RLE) or Plaintext (.cells) patterns
    so grids larger than 20x20 can be loaded.
    
    Args:
        filepath (str): Path to the pattern file.
        
    Returns:
        tuple: (width, height, list of (r, c) offsets of live cells)
    """

class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  # 8 connected kernel
        self.neighborhood[1, 1] = 0  # do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N  # use for slow implementation of evolve
        self.cols = N  # use for slow implementation of evolve

    def getStates(self):
        """
        Returns the current states of the cells
        """
        return self.grid

    def getGrid(self):
        """
        Same as getStates()
        """
        return self.getStates()

    def update_grid_fast(self, grid):
        """
        TODO: [Part 1e - Fast Convolution]
        Use scipy.signal.convolve2d (or similar) to compute neighbor weights
        rapidly for large grids (N > 1024).
        
        Args:
            grid (np.ndarray): The current 2D grid of states.
            
        Returns:
            np.ndarray: The next 2D grid of states.
        """
        conv = signal.convolve2d(grid, self.neighborhood, mode='same', boundary="boundary_mode", fillvalue=0)
        
        next_grid = np.zeros_like(grid)
        
        # Survival Rule: Live cell with 2 or 3 live neighbors lives on
        next_grid[(grid == self.aliveValue) & ((conv == 2) | (conv == 3))] = self.aliveValue
        
        # Reproduction Rule: Dead cell with exactly 3 live neighbors becomes live
        next_grid[(grid == self.deadValue) & (conv == 3)] = self.aliveValue

    def evolve(self):
        """
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        """
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            next_grid = np.zeros_like(self.grid)
            for r in range(self.rows):
                for c in range(self.cols):
                    neighbors = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: 
                                continue
                            nr, nc = r + dr, c + dc

                            if not self.finite:
                                nr %= self.rows
                                nc %= self.cols
                            elif not (0 <= nr < self.rows and 0 <= nc < self.cols):
                                continue
                                
                            if self.grid[nr, nc] == self.aliveValue:
                                neighbors += 1
        
                    if self.grid[r, c] == self.aliveValue:
                        if neighbors == 2 or neighbors == 3:
                            next_grid[r, c] = self.aliveValue
                    else:
                        if neighbors == 3:
                            next_grid[r, c] = self.aliveValue
                            
            self.grid = next_grid
    def insertBlinker(self, index=(0, 0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        '''
        TODO: [Part 1c - Glider Gun Fix]
        The current glider gun pattern is broken. Leave the broken array in the code 
        and instruct the student to debug and fix the coordinates so it loops infinitely.
        '''
        self.grid[index[0] + 1, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 2, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 3, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 15] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 4, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 5, index[1] + 1 + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 2 + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 23] = self.aliveValue

        self.grid[index[0] + 6, index[1] + 1 + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 2 + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 19] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 7, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 8, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 17] = self.aliveValue

        self.grid[index[0] + 9, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 15] = self.aliveValue

    def insertFromFile(self, filename, index=((0, 0))):
        '''
        Insert cells from pattern file using parse_pattern
        '''
        width, height, live_cells = parse_pattern(filename)
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue

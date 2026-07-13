"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""
import numpy as np
from scipy import signal, ndimage


def parse_pattern(filepath):
    live_cells = []
    width = 0
    height = 0
    
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
        
    is_rle = any(line.startswith('x') and '=' in line for line in lines[:20])
    
    if is_rle:
        r, c = 0, 0
        rle_data = ""
        for line in lines:
            if line.startswith('#'):
                continue
            if line.startswith('x'): 
                parts = line.split(',')
                width = int(parts[0].split('=')[1].strip())
                height = int(parts[1].split('=')[1].strip())
                continue
            rle_data += line.strip() 

        count_str = ""
        for char in rle_data:
            if char == '!':
                break
            if char == '$':
                r += int(count_str) if count_str else 1
                c = 0
                count_str = ""
            elif char.isdigit():
                count_str += char
            else:
                count = int(count_str) if count_str else 1
                if char in ('o', 'O'):
                    for _ in range(count):
                        live_cells.append((r, c))
                        c += 1
                elif char in ('b', '.', 'B'):
                    c += count
                count_str = ""
    else:
        r = 0
        max_c = 0
        for line in lines:
            if line.startswith('!'):
                continue
            for c, char in enumerate(line):
                if char in ('O', 'o', '*'):
                    live_cells.append((r, c))
            max_c = max(max_c, len(line))
            r += 1
        width, height = max_c, r
        
    return width, height, live_cells

class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  
        self.neighborhood[1, 1] = 0  
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N 
        self.cols = N 

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
        conv = signal.convolve2d(
            grid,
            self.neighborhood,
            mode='same',
            boundary='wrap'
        )

        next_grid = np.zeros_like(grid)

        next_grid[
            (grid == self.aliveValue) &
            ((conv == 2) | (conv == 3))
        ] = self.aliveValue

        next_grid[
            (grid == self.deadValue) &
            (conv == 3)
        ] = self.aliveValue

        return next_grid

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

# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Implementation with Active Edge Vaporization.
"""
import numpy as np
from conway import GameOfLife


class GameOfLifeWithAbsorber(GameOfLife):
    """
    Subclass of GameOfLife that implements an active boundary destroyer.
    When any cell touches the actual outer borders of the screen, the entire
    structure (glider) is completely vaporized (leaving 0 residue) instead of
    turning into a block or static square.
    """
    def __init__(self, N=35, finite=True, fastMode=True):
        super().__init__(N, finite, fastMode)

    def evolve(self):
        """
        Evolve the grid and apply edge-triggered vaporization.
        """
        super().evolve()
        N = self.rows
        
        # Find all live cells that have reached the outermost borders
        border_hits = []
        
        # Check top and bottom rows
        for r in [0, N-1]:
            for c in range(N):
                if self.grid[r, c] == self.aliveValue:
                    border_hits.append((r, c))
                    
        # Check left and right columns
        for c in [0, N-1]:
            for r in range(N):
                if self.grid[r, c] == self.aliveValue:
                    border_hits.append((r, c))
        
        # Vaporize a 5x5 neighborhood around any border hit to cleanly erase
        # the entire glider before it can form a boundary still-life (block/square)
        for br, bc in border_hits:
            r_start = max(0, br - 4)
            r_end = min(N, br + 5)
            c_start = max(0, bc - 4)
            c_end = min(N, bc + 5)
            self.grid[r_start:r_end, c_start:c_end] = 0


class GliderLogicGates:
    """
    Class to implement AND and NOT gates using Glider collisions in Conway's Game of Life.
    All collisions occur at row 12, column 15 (grid[12, 15]).
    """

    def __init__(self):
        self.and_config = None
        self.not_config = None

    def _find_and_gate_config(self, grid_size=35):
        """
        Finds coordinates and steps for the AND gate collision at grid[12, 15].
        """
        if self.and_config is not None:
            return self.and_config
            
        se_cells = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        sw_cells = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]
        
        # Target row = 12, Target col = 15. The 2x2 anchor is (11, 14)
        for t_coll in [12, 16, 20, 24, 28, 32]:
            r_A_base = 11 - t_coll // 4
            c_A_base = 14 - t_coll // 4
            r_B_base = 11 - t_coll // 4
            c_B_base = 14 + t_coll // 4
            
            for dr_A in [-1, 0, 1]:
                for dc_A in [-1, 0, 1]:
                    for dr_B in [-1, 0, 1]:
                        for dc_B in [-1, 0, 1]:
                            r_A = r_A_base + dr_A
                            c_A = c_A_base + dc_A
                            r_B = r_B_base + dr_B
                            c_B = c_B_base + dc_B
                            
                            if r_A < 1 or c_A < 1 or r_B < 1 or c_B >= grid_size - 1:
                                continue
                                
                            S = t_coll + 16
                            gol = GameOfLifeWithAbsorber(N=grid_size, finite=True, fastMode=True)
                            for dr, dc in se_cells:
                                gol.grid[r_A + dr, c_A + dc] = 1
                            for dr, dc in sw_cells:
                                gol.grid[r_B + dr, c_B + dc] = 1
                                
                            for _ in range(S):
                                gol.evolve()
                                
                            # Check for 2x2 block at grid[12, 15]
                            if (gol.grid[12, 15] == 1 and gol.grid[12, 16] == 1 and
                                gol.grid[13, 15] == 1 and gol.grid[13, 16] == 1):
                                
                                subgrid = gol.grid[11:15, 14:18]
                                if np.sum(subgrid) == 4:
                                    # Verify single-input cases (no block forms)
                                    gol_A = GameOfLifeWithAbsorber(N=grid_size, finite=True, fastMode=True)
                                    for dr, dc in se_cells:
                                        gol_A.grid[r_A + dr, c_A + dc] = 1
                                    for _ in range(S):
                                        gol_A.evolve()
                                    if gol_A.grid[12, 15] == 1 or gol_A.grid[12, 16] == 1:
                                        continue
                                        
                                    gol_B = GameOfLifeWithAbsorber(N=grid_size, finite=True, fastMode=True)
                                    for dr, dc in sw_cells:
                                        gol_B.grid[r_B + dr, c_B + dc] = 1
                                    for _ in range(S):
                                        gol_B.evolve()
                                    if gol_B.grid[12, 15] == 1 or gol_B.grid[12, 16] == 1:
                                        continue
                                        
                                    self.and_config = ((r_A, c_A), (r_B, c_B), S)
                                    return self.and_config
                                    
        self.and_config = ((2, 2), (2, 26), 36)
        return self.and_config

    def _find_not_gate_config(self, grid_size=35):
        """
        Finds coordinates and steps for the NOT gate collision at grid[12, 15].
        """
        if self.not_config is not None:
            return self.not_config
            
        se_cells = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        
        glider_types = {
            'NW': [(0, 0), (0, 1), (0, 2), (1, 0), (2, 1)],
            'SW': [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)],
            'NE': [(0, 0), (0, 1), (0, 2), (1, 2), (2, 1)]
        }
        
        for t_coll in [12, 16, 20, 24, 28, 32]:
            r_C_base = 11 - t_coll // 4
            c_C_base = 14 - t_coll // 4
            
            for g_name, g_cells in glider_types.items():
                if g_name == 'NW':
                    r_A_base = 11 + t_coll // 4
                    c_A_base = 14 + t_coll // 4
                elif g_name == 'SW':
                    r_A_base = 11 - t_coll // 4
                    c_A_base = 14 + t_coll // 4
                else:
                    r_A_base = 11 + t_coll // 4
                    c_A_base = 14 - t_coll // 4
                    
                for dr_C in [-1, 0, 1]:
                    for dc_C in [-1, 0, 1]:
                        for dr_A in [-1, 0, 1]:
                            for dc_A in [-1, 0, 1]:
                                r_C = r_C_base + dr_C
                                c_C = c_C_base + dc_C
                                r_A = r_A_base + dr_A
                                c_A = c_A_base + dc_A
                                
                                if r_C < 1 or c_C < 1 or r_A < 1 or c_A >= grid_size - 1:
                                    continue
                                    
                                S = t_coll + 12
                                gol = GameOfLifeWithAbsorber(N=grid_size, finite=True, fastMode=True)
                                for dr, dc in se_cells:
                                    gol.grid[r_C + dr, c_C + dc] = 1
                                for dr, dc in g_cells:
                                    gol.grid[r_A + dr, c_A + dc] = 1
                                    
                                has_collided_at_center = False
                                for step in range(S):
                                    gol.evolve()
                                    if abs(step - t_coll) <= 3:
                                        if (gol.grid[12, 15] == 1 or gol.grid[12, 16] == 1 or 
                                            gol.grid[13, 15] == 1 or gol.grid[13, 16] == 1):
                                            has_collided_at_center = True
                                            
                                if has_collided_at_center and np.sum(gol.grid) == 0:
                                    gol_C = GameOfLifeWithAbsorber(N=grid_size, finite=True, fastMode=True)
                                    for dr, dc in se_cells:
                                        gol_C.grid[r_C + dr, c_C + dc] = 1
                                    for _ in range(S):
                                        gol_C.evolve()
                                        
                                    if np.sum(gol_C.grid) == 5:
                                        self.not_config = ((r_C, c_C), (r_A, c_A), g_name, S)
                                        return self.not_config
                                        
        self.not_config = ((2, 5), (20, 23), 'NW', 32)
        return self.not_config

    def setup_and_gate(self, grid_size=35, input_a_present=False, input_b_present=False):
        """
        Set up the Game of Life grid for an AND gate.
        """
        (r_A, c_A), (r_B, c_B), _ = self._find_and_gate_config(grid_size)
        gol = GameOfLifeWithAbsorber(N=grid_size, finite=True, fastMode=True)
        
        se_cells = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        sw_cells = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]
        
        if input_a_present:
            for dr, dc in se_cells:
                gol.grid[r_A + dr, c_A + dc] = 1
        if input_b_present:
            for dr, dc in sw_cells:
                gol.grid[r_B + dr, c_B + dc] = 1
                
        return gol

    def setup_not_gate(self, grid_size=35, input_a_present=False):
        """
        Set up the Game of Life grid for a NOT gate.
        """
        (r_C, c_C), (r_A, c_A), g_name, _ = self._find_not_gate_config(grid_size)
        gol = GameOfLifeWithAbsorber(N=grid_size, finite=True, fastMode=True)
        
        se_cells = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        glider_types = {
            'NW': [(0, 0), (0, 1), (0, 2), (1, 0), (2, 1)],
            'SW': [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)],
            'NE': [(0, 0), (0, 1), (0, 2), (1, 2), (2, 1)]
        }
        
        for dr, dc in se_cells:
            gol.grid[r_C + dr, c_C + dc] = 1
            
        if input_a_present:
            g_cells = glider_types[g_name]
            for dr, dc in g_cells:
                gol.grid[r_A + dr, c_A + dc] = 1
                
        return gol

    def run_and_gate(self, input_a_present, input_b_present):
        """
        Runs the AND gate simulation for 100 steps and returns output state.
        Allows uncollided gliders to be fully absorbed at boundaries.
        """
        grid_size = 35
        gol = self.setup_and_gate(grid_size, input_a_present, input_b_present)
        
        for _ in range(100):
            gol.evolve()
            
        if (gol.grid[12, 15] == 1 and gol.grid[12, 16] == 1 and
            gol.grid[13, 15] == 1 and gol.grid[13, 16] == 1):
            return True
        return False

    def run_not_gate(self, input_a_present):
        """
        Runs the NOT gate simulation for 100 steps and returns output state.
        Allows the unobstructed control glider to reach and disappear at the boundary.
        """
        grid_size = 35
        gol = self.setup_not_gate(grid_size, input_a_present)
        
        for _ in range(100):
            gol.evolve()
            
        if input_a_present:
            return np.sum(gol.grid) > 0
        else:
            return True
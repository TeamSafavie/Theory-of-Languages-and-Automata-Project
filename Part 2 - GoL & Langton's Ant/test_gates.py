# -*- coding: utf-8 -*-
"""
Interactive test file with customized square-grid rendering and target highlighting.
"""
import sys
import pygame
from logic_gates import GliderLogicGates


def run_pygame_with_grid(life, cell_scale=16, fps=5, title="Game of Life"):
    """
    Renders the Game of Life simulation with clear grid lines and target highlighting.
    """
    pygame.init()
    grid = life.getStates()
    rows, cols = grid.shape
    
    # Set window size
    screen = pygame.display.set_mode((cols * cell_scale, rows * cell_scale))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                
        # 1. Fill background with black (dead cells)
        screen.fill((10, 10, 10))
        
        # 2. Draw live cells as white squares
        grid = life.getStates()
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] > 0:
                    pygame.draw.rect(
                        screen,
                        (240, 240, 240),
                        pygame.Rect(c * cell_scale, r * cell_scale, cell_scale, cell_scale)
                    )
        
        # 3. Draw grid lines to create perfect visible squares
        grid_color = (40, 40, 40)
        for x in range(0, cols * cell_scale, cell_scale):
            pygame.draw.line(screen, grid_color, (x, 0), (x, rows * cell_scale))
        for y in range(0, rows * cell_scale, cell_scale):
            pygame.draw.line(screen, grid_color, (0, y), (cols * cell_scale, y))
            
        # 4. Highlight Cartesian collision coordinate (15, 12) -> Col 15, Row 12
        target_x = 15 * cell_scale
        target_y = 12 * cell_scale
        
        # Draw a red box around the specific target cell (15, 12)
        pygame.draw.rect(
            screen,
            (255, 50, 50),
            pygame.Rect(target_x, target_y, cell_scale, cell_scale),
            2
        )
        
        # Draw a gold box around the expected 2x2 block area (15,12 to 16,13)
        pygame.draw.rect(
            screen,
            (255, 215, 0),
            pygame.Rect(target_x, target_y, cell_scale * 2, cell_scale * 2),
            1
        )
        
        pygame.display.flip()
        life.evolve()
        clock.tick(fps)
        
    pygame.quit()


def main():
    gates = GliderLogicGates()
    grid_size = 35
    cell_scale = 16
    total_simulation_steps = 100

    print("========================================")
    print("      CONWAY GLIDER LOGIC GATE TEST     ")
    print("========================================")
    print("Which gate do you want to test?")
    print("1) AND Gate")
    print("2) NOT Gate")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        print("\n--- AND Gate Configuration ---")
        in_a = input("Enter Input A (0 or 1): ").strip() == "1"
        in_b = input("Enter Input B (0 or 1): ").strip() == "1"
        
        result = gates.run_and_gate(in_a, in_b)
        print(f"\nResult: AND({int(in_a)}, {int(in_b)}) = {int(result)}")
        
        print("Launching Pygame simulation with grid lines...")
        gol = gates.setup_and_gate(grid_size, in_a, in_b)
        run_pygame_with_grid(gol, cell_scale=cell_scale, fps=5, title=f"AND Gate ({int(in_a)}, {int(in_b)})")
        
    elif choice == "2":
        print("\n--- NOT Gate Configuration ---")
        in_a = input("Enter Input A (0 or 1): ").strip() == "1"
        
        result = gates.run_not_gate(in_a)
        print(f"\nResult: NOT({int(in_a)}) = {int(result)}")
        
        print("Launching Pygame simulation with grid lines...")
        gol = gates.setup_not_gate(grid_size, in_a)
        run_pygame_with_grid(gol, cell_scale=cell_scale, fps=10, title=f"NOT Gate (Input: {int(in_a)})")
        
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
### Theory of Languages and Automata Project

This repository contains the practical assignments for the Theory of Languages
and Automata course. The project explores fundamental concepts of computation,
decidability, and emergence through mathematical models and simulations.

# The project is divided into two main parts:

1.  Turing Machines & The Busy Beaver Problem
2.  Cellular Automata (Conway's Game of Life & Langton's Ant)

📁 Project Structure

The repository is structured as follows, mirroring the two main phases of the
project:

Theory-of-Languages-and-Automata-Project/
│
├── Part 1 - Busy Beaver/
│   ├── busy_beaver.py                 # Core Busy Beaver implementations
│   ├── busy_beaver_custom.py          # Custom N-state Busy Beaver designs
│   ├── turing_machine.py              # Main Turing Machine simulator (Generator-based)
│   ├── test_*.py                      # Various unit tests (Adder, Multiplier, etc.)
│   ├── student_test_turing.py         # Self-assessment test suite
│   ├── *.pdf                          # Mathematical proofs and documentation (Turing, BB)
│   └── README.md                      # Specific details for Part 1
│
├── Part 2 - GoL & Langton's Ant/
│   ├── conway.py                      # Conway's Game of Life core logic (with SciPy convolution)
│   ├── langton.py                     # Langton's Ant core logic (Standard & Multi-color)
│   ├── logic_gates.py                 # Turing completeness proofs (AND/NOT gates via gliders)
│   ├── pygame_*.py                    # Pygame visualizers for GoL and Ant
│   ├── test_*.py                      # Unit tests for GoL, Gliders, and Logic Gates
│   ├── *.cells / *.rle                # Pattern files (Glider guns, spaceships, oscillators)
│   ├── doc.pdf                        # Project instructions and documentation
│   └── README.md                      # Specific details for Part 2
│
├── glider.pdf                         # Documentation on Glider collisions and signal processing
├── .gitignore                         
└── README.md                          # This file

🚀 Features & Implementations

Part 1: Turing Machine & Busy Beaver

  - Universal Simulator: A fully functional Turing Machine simulator implemented
    in Python using generators for memory-efficient, step-by-step execution.
  - Infinite Tape: Supports both one-way and dynamically expanding two-way
    infinite tapes.
  - Unary Arithmetic: Implemented Turing Machines capable of performing Unary
    Addition (test_turing_adder.py) and Unary Multiplication
    (test_turing_multiplier.py).
  - Busy Beaver Problem: Exploration of the Halting Problem through 2, 3, 4, 5,
    and 6-state Busy Beaver machines. Includes analysis of undecidability and
    maximum 1s generated before halting.

Part 2: Cellular Automata

  - Conway's Game of Life (GoL):
      - Core implementation with both finite and toroidal (wrapping) boundary
        conditions.
      - Optimized Execution: Uses scipy.signal.convolve2d for extremely fast
        grid updates on large matrices.
      - Pattern Parsing: Capable of reading .cells (Plaintext) and .rle
        (Run-Length Encoding) files.
  - Langton's Ant:
      - Simulates the chaotic-to-ordered emergence (the "highway").
      - Extended to support Multi-color states (e.g., LLRR, RLR) yielding
        complex symmetrical patterns.
  - Turing Completeness in GoL:
      - Proof of universality by constructing digital logic gates (AND and NOT
        gates).
      - Uses Gliders as boolean signals (presence = 1, absence = 0) and relies
        on precise collision mechanics (documented in glider.pdf).
  - Visualization: Interactive graphical interfaces built with Pygame to observe
    the automata in real-time.

⚙️ Prerequisites & Installation

To run the simulations and visualizations, you need Python 3.x installed along
with a few external libraries.

1.  Clone the repository:

```bash
    git clone https://github.com/your-username/Theory-of-Languages-and-Automata-Project.git
    cd Theory-of-Languages-and-Automata-Project
```

2.  Install the required dependencies:

```bash
    pip install numpy scipy pygame
```
    (Note: numpy and scipy are used for fast 2D convolutions in the Game of
    Life, and pygame is used for the GUI).

## 💻 How to Run

# Running Tests

Both directories contain automated test files to verify the logic. You can run
them directly via the terminal:

Part 1 Tests:

```bash
cd "Part 1 - Busy Beaver"
python test_turing_adder.py
python test_busy_beaver_2.py
python student_test_turing.py
```

Part 2 Tests:

```bash
cd "Part 2 - GoL & Langton's Ant"
python test_gameoflife_glider.py
python test_gates.py
```

### Running Visualizations (Part 2)

To see the Cellular Automata in action, run the Pygame scripts:

# Conway's Game of Life:

```bash
python pygame_gol.py
# Or to view specific patterns:
python pygame_viewer.py
```

Langton's Ant:

```bash
python langton_pygame.py
```

# 📄 Documentation

For detailed mathematical explanations, state transition tables, and algorithmic
analyses, please refer to the .pdf files located in their respective directories
(e.g., document_busy_beaver.pdf, glider.pdf).

Course: Theory of Languages and Automata
Term: 4042
University: Iran University of Science and Technology (IUST)

# 👥Development team
This project was developed by the Safavie team, which consists of two collaborators: Amirreza Moghimi([Amir-sy8](https://github.com/amir-sy8)) and Erfan Moradi([Erfan-Lab]https://github.com/Erfan-Lab).
"""Full valid 9x9 grid generation via randomized backtracking."""

import random

from .solver import is_valid_placement


def _find_empty(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def generate_full_grid():
    grid = [[0] * 9 for _ in range(9)]

    def fill():
        pos = _find_empty(grid)
        if pos is None:
            return True
        row, col = pos
        candidates = list(range(1, 10))
        random.shuffle(candidates)
        for value in candidates:
            if is_valid_placement(grid, row, col, value):
                grid[row][col] = value
                if fill():
                    return True
                grid[row][col] = 0
        return False

    fill()
    return grid

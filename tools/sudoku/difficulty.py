"""Difficulty tiers and cell-removal ("hole digging") logic."""

import random

from .solver import count_solutions

# Order matters: it's the display/generation order used everywhere else.
TIERS = [
    {"key": "facil", "label": "Fácil", "target_clues": 42},
    {"key": "medio", "label": "Medio", "target_clues": 32},
    {"key": "dificil", "label": "Difícil", "target_clues": 26},
]

TIERS_BY_KEY = {tier["key"]: tier for tier in TIERS}


def dig_holes(solution, target_clues):
    """Remove cells from a solved grid while the puzzle keeps a unique
    solution, stopping once `target_clues` is reached (or no more cells
    can be safely removed, whichever comes first)."""
    puzzle = [row[:] for row in solution]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    clues = 81

    for row, col in cells:
        if clues <= target_clues:
            break
        backup = puzzle[row][col]
        puzzle[row][col] = 0
        if count_solutions(puzzle, limit=2) == 1:
            clues -= 1
        else:
            puzzle[row][col] = backup

    return puzzle, clues

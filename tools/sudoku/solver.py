"""Backtracking sudoku solver used to generate and verify puzzles."""

BOX_STARTS = [(br, bc) for br in (0, 3, 6) for bc in (0, 3, 6)]


def _find_empty(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def is_valid_placement(grid, row, col, value):
    for i in range(9):
        if grid[row][i] == value or grid[i][col] == value:
            return False
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == value:
                return False
    return True


def count_solutions(grid, limit=2):
    """Count solutions up to `limit`, stopping early once reached."""
    working = [row[:] for row in grid]
    count = 0

    def backtrack():
        nonlocal count
        pos = _find_empty(working)
        if pos is None:
            count += 1
            return count >= limit
        row, col = pos
        for value in range(1, 10):
            if is_valid_placement(working, row, col, value):
                working[row][col] = value
                if backtrack():
                    return True
                working[row][col] = 0
        return False

    backtrack()
    return count


def solve(grid):
    """Return a solved copy of grid, or None if unsolvable."""
    working = [row[:] for row in grid]

    def backtrack():
        pos = _find_empty(working)
        if pos is None:
            return True
        row, col = pos
        for value in range(1, 10):
            if is_valid_placement(working, row, col, value):
                working[row][col] = value
                if backtrack():
                    return True
                working[row][col] = 0
        return False

    return working if backtrack() else None

class Solver:
    def __init__(self):
        self.n = 9

    def solve(self, sudoku_grid):
        solvable, solution = self.rec(sudoku_grid, 0, 0)
        if solvable:
            return solution
        return None

    def rec(self, grid, row, col):
        if row == self.n - 1 and col == self.n:
            return True, grid
        if col == self.n:
            row += 1
            col = 0
        if row == self.n or col == self.n:
            return False, grid

        if grid[row][col] > 0:
            return self.rec(grid, row, col + 1)

        for num in range(1, self.n + 1):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                s, a = self.rec(grid, row, col + 1)
                if s:
                    return True, a
            grid[row][col] = 0
        return False, grid

    def is_safe(self, grid, row, col, num):
        for x in range(self.n):
            if grid[row][x] == num or grid[x][col] == num:
                return False

        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        return True


def print_grid(arr):
    for x in arr:
        print(x)


if __name__ == '__main__':
    test_grid = [
        [0, 0, 0, 8, 0, 3, 0, 5, 0],
        [2, 4, 0, 0, 9, 5, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 4, 0, 0, 8],
        [0, 0, 6, 3, 0, 0, 4, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 7, 0, 5, 0, 0, 0, 9, 0],
        [0, 5, 0, 0, 0, 0, 7, 2, 0],
        [0, 2, 0, 0, 8, 1, 0, 0, 0]
    ]
    solver = Solver()
    print_grid(solver.solve(test_grid))

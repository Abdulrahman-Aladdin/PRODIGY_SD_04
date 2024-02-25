import customtkinter as ctk
from settings import *


class Square(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color=SQUARE_FG, corner_radius=CORNER_RADIUS)
        self.rowconfigure((0, 1, 2), weight=1, uniform='c')
        self.columnconfigure((0, 1, 2), weight=1, uniform='d')


class GridLabel(ctk.CTkLabel):
    def __init__(self, master, activate, row, col):
        super().__init__(master=master, text='', font=ctk.CTkFont(size=FONT_SIZE, family=FONT), fg_color=CELL_FG,
                         width=CELL_SIZE, height=CELL_SIZE, corner_radius=CORNER_RADIUS, text_color=TEXT_COLOR)
        self.row = row
        self.col = col
        self.bind('<Button>', lambda e: activate(self.row, self.col))


class GridFrame(ctk.CTkFrame):
    def __init__(self, master, solver):
        super().__init__(master=master, fg_color=GRID_FRAME_FG, corner_radius=CORNER_RADIUS)

        self.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='b')

        self.cur_row = 0
        self.cur_col = 0
        self.active = True

        self.nums_grid = [[0 for _ in range(9)] for _ in range(9)]

        self.squares = [[Square(self) for _ in range(3)] for _ in range(3)]
        self.place_squares()

        self.grid_labels = [[GridLabel(self.squares[i // 3][j // 3], self.activate, i, j)
                             for j in range(9)] for i in range(9)]
        self.grid_labels[0][0].configure(fg_color=ACTIVE_CELL_FG)
        self.place_labels()

        self.solver = solver

    def is_safe(self, num):
        for x in range(9):
            if self.nums_grid[self.cur_row][x] == num or self.nums_grid[x][self.cur_col] == num:
                return False

        start_row = self.cur_row - self.cur_row % 3
        start_col = self.cur_col - self.cur_col % 3
        for i in range(3):
            for j in range(3):
                if self.nums_grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def place_squares(self):
        for row in range(3):
            for col in range(3):
                self.squares[row][col].grid(row=row, column=col, padx=SQUARE_GAP, pady=SQUARE_GAP)

    def place_labels(self):
        for row in range(9):
            for col in range(9):
                self.grid_labels[row][col].grid(row=row % 3, column=col % 3, padx=CELL_GAP, pady=CELL_GAP)

    def reset(self):
        for i in range(9):
            for j in range(9):
                self.grid_labels[i][j].configure(text='', fg_color=CELL_FG)
                self.nums_grid[i][j] = 0
        self.active = True
        self.activate(0, 0)

    def action(self, e):
        if self.active:
            code = e.keycode
            if self.is_digit(code):
                self.set_label(e.char)
            elif self.is_movement(code):
                self.move_cur(code)
            elif self.is_solve(code):
                self.solve()
            elif self.is_delete(code):
                self.set_label('')
            else:
                self.error_flag()

    def solve(self):
        self.active = False
        ans = self.solver(self.nums_grid)
        if ans is not None:
            self.set_solution(ans)
        else:
            self.active = True

    def error_flag(self):
        def flash_color(count):
            if count < 6:
                self.grid_labels[self.cur_row][self.cur_col].configure(
                    fg_color='red' if count % 2 == 0 else ACTIVE_CELL_FG)
                self.after(75, flash_color, count + 1)
            else:
                self.grid_labels[self.cur_row][self.cur_col].configure(fg_color=ACTIVE_CELL_FG)
                self.active = True

        self.active = False
        flash_color(0)

    def move_cur(self, code):
        dx, dy = 0, 0
        if code == LEFT:
            dx = -1
        elif code == RIGHT:
            dx = 1
        elif code == UP:
            dy = -1
        else:
            dy = 1
        self.activate((self.cur_row + dy) % 9, (self.cur_col + dx) % 9)

    def set_label(self, digit):
        if digit == '':
            self.grid_labels[self.cur_row][self.cur_col].configure(text=digit)
            self.nums_grid[self.cur_row][self.cur_col] = 0
        elif self.is_safe(int(digit)):
            self.grid_labels[self.cur_row][self.cur_col].configure(text=digit)
            self.nums_grid[self.cur_row][self.cur_col] = int(digit)
        else:
            self.error_flag()

    def activate(self, row, col):
        if self.active:
            self.grid_labels[self.cur_row][self.cur_col].configure(fg_color=CELL_FG)
            self.cur_row = row
            self.cur_col = col
            self.grid_labels[row][col].configure(fg_color=ACTIVE_CELL_FG)

    def set_solution(self, ans):
        self.grid_labels[self.cur_row][self.cur_col].configure(fg_color=CELL_FG)
        for i in range(9):
            for j in range(9):
                self.grid_labels[i][j].configure(text=str(ans[i][j]), fg_color='#126456')
        self.active = False

    @staticmethod
    def is_digit(n):
        return 97 <= n <= 105 or 49 <= n <= 57

    @staticmethod
    def is_movement(n):
        return 37 <= n <= 40

    @staticmethod
    def is_solve(n):
        return n == SOLVE

    @staticmethod
    def is_delete(n):
        return n in DELETE

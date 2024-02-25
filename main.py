import customtkinter as ctk
from settings import *
from GuiUtils import GridFrame
from PuzzleSolver import Solver


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.geometry(f'{WINDOW_SIZE}x{WINDOW_SIZE}')
        self.minsize(WINDOW_SIZE, WINDOW_SIZE)
        self.configure(fg_color=WINDOW_FG)
        self.resizable(RESIZABLE, RESIZABLE)

        ctk.CTkLabel(master=self, text=TITLE,
                     font=ctk.CTkFont(family=FONT, size=FONT_SIZE, weight='bold')).pack(fill='both', pady=10)

        self.comments_var = ctk.StringVar(value='Enter the puzzle!')
        self.comments_label = ctk.CTkLabel(master=self, textvariable=self.comments_var,
                                           font=ctk.CTkFont(family=FONT, size=FONT_SIZE_A))

        self.reset_btn = ctk.CTkButton(master=self, text='New Game!', command=self.reset,
                                       font=ctk.CTkFont(family=FONT, size=FONT_SIZE_A),
                                       fg_color=BTN_FG, hover_color=BTN_HVR)

        self.solver = Solver()

        self.grid_container = ctk.CTkFrame(master=self, fg_color='transparent')
        self.grid_frame = GridFrame(self.grid_container, self.solve)
        self.bind('<Key>', self.grid_frame.action)
        self.grid_frame.place(relx=.5, rely=.5, anchor='center')

        self.grid_container.pack(fill='both', expand=True)

        self.comments_label.pack(fill='both', pady=10)

        self.mainloop()

    def reset(self):
        self.grid_frame.reset()
        self.reset_btn.pack_forget()
        self.comments_var.set('Enter the puzzle!')
        self.comments_label.pack(fill='both', pady=10)

    def solve(self, grid):
        ans = self.solver.solve(grid)
        if ans is not None:
            self.comments_label.pack_forget()
            self.reset_btn.pack(ipadx=2, ipady=2, pady=10)
            return ans
        else:
            self.comments_var.set('Unsolvable!!')


if __name__ == '__main__':
    App()

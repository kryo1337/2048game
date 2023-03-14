import tkinter as tk
import random
import colors as c
from GUI import GUI


class Gameplay(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        gui = GUI()
        self.matrix = None
        self.score = None
        self.cells, self.score_label, self.main_grid = gui.make_GUI()

        self.start_game(self.cells)

        self.master.bind("<a>", self.left)
        self.master.bind("<d>", self.right)
        self.master.bind("<w>", self.up)
        self.master.bind("<s>", self.down)

        self.mainloop()

    def start_game(self, cells):
        self.matrix = [[0] * 4 for _ in range(4)]
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")

        self.score = 0

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value], fg=c.CELL_NUMBER_COLORS[cell_value], font=c.CELL_NUMBER_FONTS[cell_value], text=str(cell_value))
        self.score_label.configure(text=self.score)


    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        if any(0 in row for row in self.matrix):
            self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        if any(0 in row for row in self.matrix):
            self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        if any(0 in row for row in self.matrix):
            self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        if any(0 in row for row in self.matrix):
            self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You win!", bg=c.WINNER_BG, fg=c.GAME_OVER_FONT_COLOR, font=c.GAME_OVER_FONT)
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="Game over!", bg=c.LOSER_BG, fg=c.GAME_OVER_FONT_COLOR, font=c.GAME_OVER_FONT)

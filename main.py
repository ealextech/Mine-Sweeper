import tkinter as tk
import random


class MinesweeperGame:
    def __init__(self, master, rows, columns, mines):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.buttons = []
        self.minefield = []
        self.game_over = False

        self.create_minefield()
        self.place_mines()
        self.calculate_numbers()
        self.create_buttons()

    def create_minefield(self):
        self.minefield = [[0] * self.columns for _ in range(self.rows)]

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.columns - 1)
            if self.minefield[row][col] != -1:
                self.minefield[row][col] = -1
                mines_placed += 1

    def calculate_numbers(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.minefield[row][col] == -1:
                    continue
                count = 0
                for i in range(max(0, row - 1), min(row + 2, self.rows)):
                    for j in range(max(0, col - 1), min(col + 2, self.columns)):
                        if self.minefield[i][j] == -1:
                            count += 1
                self.minefield[row][col] = count

    def create_buttons(self):
        for row in range(self.rows):
            button_row = []
            for col in range(self.columns):
                button = tk.Button(self.master, width=2, height=1)
                button.grid(row=row, column=col, padx=1, pady=1)
                button.bind('<Button-1>', lambda event, r=row, c=col: self.on_left_click(r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.on_right_click(r, c))
                button_row.append(button)
            self.buttons.append(button_row)

    def on_left_click(self, row, col):
        if self.game_over:
            return

        button = self.buttons[row][col]
        value = self.minefield[row][col]

        if value == -1:
            self.reveal_mines()
            self.game_over = True
            self.show_game_over_message("Hai perso!")
        elif value == 0:
            self.reveal_empty_cells(row, col)
        else:
            button.config(text=str(value), state=tk.DISABLED)

    def on_right_click(self, row, col):
        if self.game_over:
            return

        button = self.buttons[row][col]

        if button['state'] == tk.NORMAL:
            button.config(text="🚩")
        elif button['state'] == tk.DISABLED:
            button.config(text="")

    def reveal_empty_cells(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.columns:
            return

        button = self.buttons[row][col]
        value = self.minefield[row][col]

        if button['state'] == tk.DISABLED:
            return

        if value == -1:
            return

        button.config(text=str(value), state=tk.DISABLED)

        if value == 0:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    self.reveal_empty_cells(i, j)

    def reveal_mines(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.minefield[row][col] == -1:
                    button = self.buttons[row][col]
                    button.config(text="💣", state=tk.DISABLED)

    def show_game_over_message(self, message):
        popup = tk.Toplevel()
        popup.title("Game Over")
        label = tk.Label(popup, text=message)
        label.pack()
        button = tk.Button(popup, text="Chiudi", command=self.master.destroy)
        button.pack()


def play_minesweeper(rows, columns, mines):
    root = tk.Tk()
    root.title("Minesweeper")
    game = MinesweeperGame(root, rows, columns, mines)
    root.mainloop()


# Esempio di utilizzo
play_minesweeper(rows=10, columns=10, mines=10)

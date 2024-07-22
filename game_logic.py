# game_logic.py

import random

class Game2048:
    def __init__(self):
        self.grid = [[0]*4 for _ in range(4)]
        self.movement_data = []
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4
            self.movement_data.append((r, c, 'new'))

    def can_merge(self, a, b):
        return a == b and a != 0

    def slide_row_left(self, row, row_idx):
        new_row = [i for i in row if i != 0]
        while len(new_row) < 4:
            new_row.append(0)
        for i in range(3):
            if self.can_merge(new_row[i], new_row[i + 1]):
                new_row[i] *= 2
                new_row[i + 1] = 0
                self.score += new_row[i]  # Increase score
                self.movement_data.append((row_idx, i, 'merge'))
        new_row = [i for i in new_row if i != 0]
        while len(new_row) < 4:
            new_row.append(0)
        return new_row

    def move_left(self):
        self.movement_data = []
        new_grid = []
        for row_idx, row in enumerate(self.grid):
            new_row = self.slide_row_left(row, row_idx)
            new_grid.append(new_row)
            for col_idx in range(4):
                if row[col_idx] != new_row[col_idx]:
                    self.movement_data.append((row_idx, col_idx, 'move'))
        if new_grid != self.grid:
            self.grid = new_grid
            self.add_new_tile()
            return True
        return False

    def move_right(self):
        self.grid = [row[::-1] for row in self.grid]
        moved = self.move_left()
        self.grid = [row[::-1] for row in self.grid]
        return moved

    def move_up(self):
        self.grid = list(map(list, zip(*self.grid)))
        moved = self.move_left()
        self.grid = list(map(list, zip(*self.grid)))
        return moved

    def move_down(self):
        self.grid = list(map(list, zip(*self.grid)))
        moved = self.move_right()
        self.grid = list(map(list, zip(*self.grid)))
        return moved

    def is_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False
        for r in range(4):
            for c in range(4):
                if r < 3 and self.grid[r][c] == self.grid[r + 1][c]:
                    return False
                if c < 3 and self.grid[r][c] == self.grid[r][c + 1]:
                    return False
        return True

    def reset_game(self):
        self.__init__()

    def print_grid(self):
        for row in self.grid:
            print(row)
        print()

import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:

        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    r = random.choice([0, 1])
                    grid[i][j] = r
        else:
            return grid
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        neibors = []
        for d in directions:
            h = cell[0] + d[0]
            w = cell[1] + d[1]
            if (0 <= h < self.rows) and (0 <= w < self.cols):
                neibors.append(self.curr_generation[h][w])
        return neibors

    def get_next_generation(self) -> Grid:
        next_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                count_of_neighbours = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1:
                    if count_of_neighbours == 2 or count_of_neighbours == 3:
                        next_grid[i][j] = 1
                else:
                    if count_of_neighbours == 3:
                        next_grid[i][j] = 1
        self.prev_generation = self.curr_generation
        self.curr_generation = next_grid

        return self.curr_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            if self.max_generations > self.generations:
                return False
        return True

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        # text = pathlib.Path.cwd() / "grid.txt"
        t = filename.read_text()
        grid = []
        for line in t.split("\n"):
            grid_row = []
            for el in line:
                grid_row.append(int(el))
            if len(grid_row) > 0:
                grid.append(grid_row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        for i in range(len(self.curr_generation)):
            filename.write_text("".join(str(el) for el in self.curr_generation[i]) + "\n")

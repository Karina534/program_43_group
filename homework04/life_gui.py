import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.life.rows))
        for y in range(0, self.life.rows, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.life.cols, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        pass

    def run(self) -> None:
        # Copy from previous assignment
        pass

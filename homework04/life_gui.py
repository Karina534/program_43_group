import pathlib

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        self.pause = False

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size),
                    )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.pause = not self.pause
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        cell_x = x // self.cell_size
                        cell_y = y // self.cell_size
                        if self.life.curr_generation[cell_x][cell_y] == 1:
                            self.life.curr_generation[cell_x][cell_y] = 0
                            pygame.draw.rect(
                                self.screen,
                                pygame.Color("white"),
                                (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size),
                            )
                        else:
                            self.life.curr_generation[cell_x][cell_y] = 1
                            pygame.draw.rect(
                                self.screen,
                                pygame.Color("green"),
                                (cell_x * self.cell_size, cell_y * self.cell_size, self.cell_size, self.cell_size),
                            )

            if not self.pause:
                self.draw_grid()
                self.life.step()
                self.draw_lines()

            if self.life.is_max_generations_exceeded or not self.life.is_changing:
                running = False

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((50, 50), max_generations=100)
    ui = GUI(life)
    ui.run()

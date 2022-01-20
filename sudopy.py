import pygame
import sys
import math
from dataclasses import dataclass


W_SIZE = W_WIDTH, W_HEIGHT = 800, 800


@dataclass(frozen=True)
class Color:
    WHITE: tuple = 255, 255, 255
    BLACK: tuple = 0, 0, 0
    RED: tuple = 255, 0, 0
    GREEN: tuple = 0, 255, 0
    BLUE: tuple = 0, 0, 255
    LIGHTBLUE: tuple = 186, 226, 224


class Cell:
    def __init__(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        value: int,
        selected: bool = False,
        given: bool = False,
        correct: bool = False,
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = value
        self.selected = selected
        self.given = given
        self.correct = correct

    def render(self, surface: pygame.surface.Surface, font: pygame.font.Font) -> None:
        color = Color.LIGHTBLUE if self.selected else Color.WHITE
        pygame.draw.rect(surface, color, pygame.Rect(self.x, self.y, self.w, self.h))

        font_color = Color.BLACK

        if self.given:
            font_color = Color.BLUE
        elif not self.correct:
            font_color = Color.RED

        if self.value != 0:
            text = font.render(str(self.value), True, font_color)
            text_rect = text.get_rect(center=(self.x + self.w / 2, self.y + self.h / 2))
            surface.blit(text, text_rect)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def set_value(self, value: int):
        self.value = value


def generate_grid(state: list[int], size: float, spacing: float) -> list[Cell]:
    x, y = spacing, spacing
    grid = []

    for i in range(9):
        for j in range(9):
            value = state[(i * 9) + j]
            is_given = False if value == 0 else True

            new_cell = Cell(x, y, size, size, value, False, is_given)
            grid.append(new_cell)

            x += size + spacing

        y += size + spacing
        x = spacing

    return grid


def draw_board(
    surface: pygame.surface.Surface, font: pygame.font.Font, grid: list[Cell]
) -> None:
    # Outlines
    # pygame.draw.line(surface, Color.BLACK, (0, 0), (W_WIDTH, 0), 2)
    # pygame.draw.line(
    # surface, Color.BLACK, (0, W_HEIGHT - 2), (W_WIDTH - 2, W_HEIGHT - 2), 2
    # )
    # pygame.draw.line(surface, Color.BLACK, (0, 0), (0, W_HEIGHT), 2)
    # pygame.draw.line(surface, Color.BLACK, (W_WIDTH - 2, 0), (W_WIDTH - 2, W_HEIGHT), 2)

    # Grid

    for cell in grid:
        cell.render(surface, font)


def main() -> None:
    pygame.init()

    NUMBER_KEYS = {
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 4,
        pygame.K_5: 5,
        pygame.K_6: 6,
        pygame.K_7: 7,
        pygame.K_8: 8,
        pygame.K_9: 9,
    }

    # fmt: off
    state = [
        5, 3, 0, 0, 7, 0, 0, 0, 0,
        6, 0, 0, 1, 9, 5, 0, 0, 0,
        0, 9, 8, 0, 0, 0, 0, 6, 0,
        8, 0, 0, 0, 6, 0, 0, 0, 3,
        4, 0, 0, 8, 0, 3, 0, 0, 1,
        7, 0, 0, 0, 2, 0, 0, 0, 6,
        0, 6, 0, 0, 0, 0, 2, 8, 0,
        0, 0, 0, 4, 1, 9, 0, 0, 5,
        0, 0, 0, 0, 8, 0, 0, 7, 9
    ]
    # fmt: on

    cell_scale = 87.9
    spacing = 1

    grid = generate_grid(state, cell_scale, spacing)

    screen = pygame.display.set_mode(W_SIZE)

    font = pygame.font.Font(pygame.font.get_default_font(), 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    selected_index = (
                        math.floor(mouse_x / cell_scale)
                        + math.floor(mouse_y / cell_scale) * 9
                    )
                    print(selected_index)

                    for cell_index in range(len(grid)):
                        if cell_index == selected_index:
                            grid[cell_index].select()
                        else:
                            grid[cell_index].deselect()
            if event.type == pygame.KEYDOWN:
                if event.key in NUMBER_KEYS:
                    for cell in grid:
                        if cell.selected:
                            cell.set_value(NUMBER_KEYS[event.key])

        screen.fill(Color.BLACK)

        draw_board(screen, font, grid)

        pygame.display.flip()


if __name__ == "__main__":
    main()

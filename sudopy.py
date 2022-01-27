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
    ) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = value
        self.selected = selected
        self.given = given
        self.correct = correct

    def __eq__(self, other: "Cell") -> bool:
        return self.x == other.x and self.y == other.y

    def render(self, surface: pygame.surface.Surface, font: pygame.font.Font) -> None:
        color = Color.LIGHTBLUE if self.selected else Color.WHITE
        pygame.draw.rect(surface, color, pygame.Rect(self.x, self.y, self.w, self.h))

        font_color = Color.BLUE

        if self.given:
            font_color = Color.BLACK
        elif not self.correct:
            font_color = Color.RED

        if self.value != 0:
            text = font.render(str(self.value), True, font_color)
            text_rect = text.get_rect(center=(self.x + self.w / 2, self.y + self.h / 2))
            surface.blit(text, text_rect)

    def select(self) -> None:
        self.selected = True

    def deselect(self) -> None:
        self.selected = False

    def set_value(self, value: int) -> None:
        self.value = value

    def get_value(self) -> int:
        return self.value

    def erase(self) -> None:
        self.value = 0

    def is_selected(self) -> bool:
        return self.selected

    def is_given(self) -> bool:
        return self.given

    def set_correct(self) -> None:
        self.correct = True

    def set_wrong(self) -> None:
        self.correct = False

    def is_correct(self) -> bool:
        return self.correct


def select_cell(cell: Cell, grid: list[Cell]) -> None | Cell:
    to_return = None

    if not cell.is_selected():
        cell.select()
        to_return = cell
    else:
        cell.deselect()

    for other_cell in grid:
        if other_cell != cell:
            other_cell.deselect()

    return to_return


def check_correctness(cell: Cell, grid: list[Cell], solution: list[int]) -> None:
    cell_index = grid.index(cell)

    if solution[cell_index] == cell.get_value():
        cell.set_correct()
    else:
        cell.set_wrong()


def handle_value(
    cell: Cell,
    valid_keys: dict,
    key_pressed: int,
    grid: list[Cell],
    solution: list[int],
) -> None:
    cell.set_value(valid_keys[key_pressed])
    check_correctness(cell, grid, solution)


def handle_keypress(
    cell: Cell | None,
    valid_keys: dict,
    key_pressed: int,
    grid: list[Cell],
    solution: list[int],
) -> None:
    if cell and not (cell.is_given() or cell.is_correct()):
        if key_pressed in valid_keys:
            handle_value(cell, valid_keys, key_pressed, grid, solution)
        elif key_pressed in (pygame.K_DELETE, pygame.K_BACKSPACE):
            cell.erase()


def generate_grid(
    state: list[int],
    size: float,
    lg_spacing: float,
    md_spacing: float,
    sm_spacing: float,
) -> list[Cell]:
    x, y = md_spacing, md_spacing
    grid = []

    for i in range(9):
        for j in range(9):
            value = state[(i * 9) + j]
            is_given = False if value == 0 else True

            new_cell = Cell(x, y, size, size, value, False, is_given)
            grid.append(new_cell)

            if j != 8 and (j + 1) % 3 == 0:
                x += size + lg_spacing
            else:
                x += size + sm_spacing

        if i != 8 and (i + 1) % 3 == 0:
            y += size + lg_spacing
        else:
            y += size + sm_spacing

        x = md_spacing

    return grid


def draw_board(
    surface: pygame.surface.Surface, font: pygame.font.Font, grid: list[Cell]
) -> None:
    for cell in grid:
        cell.render(surface, font)


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode(W_SIZE)
    font = pygame.font.Font(pygame.font.get_default_font(), 50)

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
    solution = [
        5, 3, 4, 6, 7, 8, 9, 1, 2,
        6, 7, 2, 1, 9, 5, 3, 4, 8,
        1, 9, 8, 3, 4, 2, 5, 6, 7,
        8, 5, 9, 7, 6, 1, 4, 2, 3,
        4, 2, 6, 8, 5, 3, 7, 9, 1,
        7, 1, 3, 9, 2, 4, 8, 5, 6,
        9, 6, 1, 5, 3, 7, 2, 8, 4,
        2, 8, 7, 4, 1, 9, 6, 3, 5,
        3, 4, 5, 2, 8, 6, 1, 7, 9
    ]
    # fmt: on

    lg_spacing = 3
    md_spacing = 2
    sm_spacing = 1

    cell_scale = (W_WIDTH - (lg_spacing * 2) - (md_spacing * 2) - (sm_spacing * 6)) / 9

    grid = generate_grid(state, cell_scale, lg_spacing, md_spacing, sm_spacing)

    selected_cell = None

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

                    selected_cell = grid[selected_index]
                    selected_cell = select_cell(selected_cell, grid)

            if event.type == pygame.KEYDOWN:
                handle_keypress(selected_cell, NUMBER_KEYS, event.key, grid, solution)

        screen.fill(Color.BLACK)

        draw_board(screen, font, grid)

        pygame.display.flip()


if __name__ == "__main__":
    main()

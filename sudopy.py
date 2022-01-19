import pygame
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    WHITE: tuple = 255, 2555, 2555
    BLACK: tuple = 0, 0, 0
    RED: tuple = 255, 0, 0
    GREEN: tuple = 0, 255, 0
    BLUE: tuple = 0, 0, 255


def main() -> None:
    WINDOW_SIZE = 800, 600

    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(Color.BLACK)


if __name__ == "__main__":
    main()

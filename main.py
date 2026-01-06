import pygame
from settings import window
from menu import main_menu
from game import main_game


def main(window):
    while True:
        start_game = main_menu(window)
        if not start_game:
            break
        back_to_menu = main_game(window)
        if not back_to_menu:
            break
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)

# shootout_game_mvc/
# ├── main.py          -> entry point (controller)
# ├── model.py         -> game logic (weapons, players, actions)
# ├── view.py          -> Pygame GUI rendering
# └── constants.py     -> enums, decision matrix, colors

# main.py
import pygame
import sys
from model import Game
from view import GameView

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Shootout Game (MVC Edition)")
clock = pygame.time.Clock()


def main():
    game = Game()
    view = GameView(game, screen)

    running = True
    while running:
        clock.tick(30)
        view.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                view.check_click(pygame.mouse.get_pos())

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

# You should split model.py, view.py, and constants.py into their own files accordingly.

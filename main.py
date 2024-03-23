# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pygame
from board import Board


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1080, 620))
    board = Board(10, screen, 1080, 620)
    while(True):
        board.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                screen.fill((0, 0, 0))
                if event.key == pygame.K_m:
                    board.move("up", 2)
                if event.key == pygame.K_s:
                    board.sense()
                if event.key == pygame.K_g:
                    print(board.get_position())
        pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

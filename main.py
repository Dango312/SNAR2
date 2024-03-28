import random
import pygame
from SNAR2.board import Board


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1080, 620))
    board = Board(5, screen, 1080, 620)
    direction = ["up", "down", "right", "left"]
    while(True):
        board.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                screen.fill((0, 0, 0))
                if event.key == pygame.K_m:  # при нажатии m робот перемещается в случайную сторону
                    board.move(direction[random.randint(0, 3)], random.randint(1, 3))
                if event.key == pygame.K_s:  # при нажатии клавиши s вычисляются вероятности после sense
                    board.sense()
                if event.key == pygame.K_g:  # при нажатии g выводится наиболее вероятная координата робота
                    print(board.get_position())
        pygame.display.update()


if __name__ == '__main__':
    main()
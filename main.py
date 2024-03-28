import random
import pygame
from board import Board
import moviepy.editor

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1080, 620))



    #Отрисовка кнопок меню
    font = pygame.font.SysFont("Comic Sans MS", 20)
    lable_font = pygame.font.SysFont("Comic Sans MS", 50)
    text_uniform = font.render('Uniform Mode', True, WHITE)
    text_definite = font.render('Definite Mode', True, WHITE)
    text_map = font.render('Draw Map', True, WHITE)
    text_authors = font.render("Auhors: Mankevich Sergey, Karpov Eduard", False, (255, 255, 255))
    text_lable = lable_font.render("My Little Robot", False, (255, 20, 147))
    text_input = font.render("Enter map size (e.g., 5):", True, WHITE)
    # Расположение кнопок меню
    button_uniform = text_uniform.get_rect(center=(150, 50))
    button_definite = text_definite.get_rect(center=(300, 50))
    button_map = text_map.get_rect(center=(450, 50))
    input_box = pygame.Rect(300, 100, 140, 32)
    #board = Board(10, screen, 1080, 620)
    board = None
    direction = ["up", "down", "right", "left"]
    menu_flag = True
    mode = 'uniform'
    map_size = 10
    active = False
    text = ''
    count_K = 0
    while(True):
        if menu_flag:
            screen.fill(BLACK)
            # Рисуем меню
            pygame.draw.rect(screen, GRAY, button_uniform)
            pygame.draw.rect(screen, GRAY, button_definite)
            pygame.draw.rect(screen, GRAY, button_map)
            screen.blit(text_uniform, button_uniform)
            screen.blit(text_definite, button_definite)
            screen.blit(text_map, button_map)
            screen.blit(text_authors, (50, 500))
            screen.blit(text_lable, (300, 200))
            screen.blit(text_input, (50, 100))
            txt_surface = font.render(text, True, WHITE)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, WHITE, input_box, 2)
        elif map_size == 6 or showVideo:

            showVideo = False
        else:
            board.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_uniform.collidepoint(event.pos):
                    mode = 'uniform'
                elif button_definite.collidepoint(event.pos):
                    mode = 'definite'
                elif button_map.collidepoint(event.pos):
                    # Отрисовываем карту
                    if board is None:
                        board = Board(map_size, screen, 1080, 620, mode)
                        menu_flag = False
                    board.draw()
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                screen.fill((0, 0, 0))
                if event.key == pygame.K_m:  # при нажатии m робот перемещается в случайную сторону
                    board.move(direction[random.randint(0, 3)], random.randint(1, 3))
                if event.key == pygame.K_s:  # при нажатии клавиши s вычисляются вероятности после sense
                    board.sense()
                if event.key == pygame.K_g:  # при нажатии g выводится наиболее вероятная координата робота
                    print(board.get_position())
                if event.key == pygame.K_r:
                    count_K+=1
                    if count_K == 6:
                        video = moviepy.editor.VideoFileClip("Creepy Grudge Ghost Girl in the Mirror-.mp4")
                        video.preview()
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        map_size = int(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        pygame.display.update()


if __name__ == '__main__':
    main()
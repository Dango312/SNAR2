import pygame
import random
import math
import numpy as np

class Board(object):
    def __init__(self, size, screen, width, height):
        self.board = []
        self.probs = np.zeros((size, size))
        self.map = []
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.size = size
        self.p_move = [
            [0.0, 0.1, 0.0],
            [0.1, 0.8, 0.1],
            [0.0, 0.1, 0.0]
        ]

        self.w = height // size
        self.h = height // size
        x_r = math.floor(random.random()*size)
        y_r = math.floor(random.random()*size)
        self.probs[y_r, x_r] = 1.0
        self.robot = Robot(x_r*self.w + self.w // 2, y_r*self.h + self.h//2, x_r, y_r, math.floor(self.w*0.3), height, size, screen)
        self.logger = Logger(screen, height+80, 40)
        for i in range(size):
            row = []
            map_row = []
            for j in range(size):
                x = j*self.w
                y = i*self.h
                if random.random() > 0.5:
                    row.append(Tile(self.red, x, y, self.w, self.h, screen))
                    map_row.append("red")
                else:
                    row.append(Tile(self.green, x, y, self.w, self.h, screen))
                    map_row.append("green")
            self.board.append(row)
            self.map.append(map_row)

        self.logger.draw()

    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].draw()
        self.logger.draw_probs(self.probs)
        self.robot.draw()

    def move(self, direction, distance):
        new_probabilities = np.zeros((self.size, self.size))

        d_x = 0
        d_y = 0

        p_mv = random.random()

        if direction == "up":
            if p_mv < self.p_move[1][1]:
                d_y = distance
            elif p_mv - self.p_move[1][1] < self.p_move[0][1]:
                d_y = distance+1
            else:
                d_y = distance-1
        elif distance == "down":
            if p_mv < self.p_move[1][1]:
                d_y = distance
            elif p_mv - self.p_move[1][1] < self.p_move[0][1]:
                d_y = distance-1
            else:
                d_y = distance+1
        elif distance == "right":
            if p_mv < self.p_move[1][1]:
                d_x = distance
            elif p_mv - self.p_move[1][1] < self.p_move[1][0]:
                d_x = distance - 1
            else:
                d_x = distance + 1
        elif distance == "left":
            if p_mv < self.p_move[1][1]:
                d_x = distance
            elif p_mv - self.p_move[1][1] < self.p_move[1][0]:
                d_x = distance + 1
            else:
                d_x = distance - 1

        self.robot.move(d_x*self.w, d_y*self.h, d_x, d_y)

        for x in range(self.size):
            for y in range(self.size):
                # new_x = x + dx * distance
                # new_y = y + dy * distance

                if direction == 'up':
                    new_probabilities[y, x] += self.probs[(y - distance) % self.size, x] * self.p_move[1][1]
                    new_probabilities[y, x] += self.probs[(y - distance + 1) % self.size, x] * self.p_move[0][1]
                    new_probabilities[y, x] += self.probs[(y - distance - 1) % self.size, x] * self.p_move[2][1]
                elif direction == 'down':
                    new_probabilities[y, x] += self.probs[(y + distance) % self.size, x] * self.p_move[1][1]
                    new_probabilities[y, x] += self.probs[(y + distance + 1) % self.size, x] * self.p_move[2][1]
                    new_probabilities[y, x] += self.probs[(y + distance - 1) % self.size, x] * self.p_move[0][1]
                elif direction == 'left':
                    new_probabilities[y, x] += self.probs[y, (x - distance) % self.size] * self.p_move[1][1]
                    new_probabilities[y, x] += self.probs[y, (x - distance + 1) % self.size] * self.p_move[1][0]
                    new_probabilities[y, x] += self.probs[y, (x - distance - 1) % self.size] * self.p_move[1][2]
                elif direction == 'right':
                    new_probabilities[y, x] += self.probs[y, (x + distance) % self.size] * self.p_move[1][1]
                    new_probabilities[y, x] += self.probs[y, (x + distance + 1) % self.size] * self.p_move[1][2]
                    new_probabilities[y, x] += self.probs[y, (x + distance - 1) % self.size] * self.p_move[1][0]

        self.probs = new_probabilities / np.sum(new_probabilities)
        self.logger.draw_probs(self.probs)

    def sense(self):
        x = self.robot.x_i
        y = self.robot.y_i
        print("X, Y", x, y)
        color = self.map[y][x]
        real_sensor_error = 1
        correct_detection = 0.6
        incorrect_detection = 0.2
        print("ЦВЕТА: ", color)
        flag = random.random() < real_sensor_error
        print('Flag = ', flag)
        if not flag:
            color = 'red' if color == 'green' else 'green'
        for i in range(self.size):
            for j in range(self.size):
                print('Is equal: ', i, j, self.map[i][j] == color)
                if self.map[i][j] == color:
                    self.probs[i, j] *= correct_detection
                else:
                    self.probs[i, j] *= incorrect_detection

        self.probs /= np.sum(self.probs)
        print("After sense:\n", self.probs)

    def get_position(self):
        return np.unravel_index(np.argmax(self.probs), self.probs.shape)


class Tile(object):
    def __init__(self, color, x, y, w, h, screen):
        self.color = color
        self.pos = (x, y)
        self.rect = pygame.Rect((x, y), (w, h))
        self.screen = screen

    def draw(self):
        pygame.draw .rect(self.screen, self.color, self.rect)


class Robot(object):
    def __init__(self, x, y, x_i, y_i, w, height, size, screen):
        self.x = x
        self.y = y
        self.x_i = x_i
        self.y_i = y_i
        self.w = w
        self.screen = screen
        self.height = height
        self.size = size

    def move(self, d_x, d_y, d_x_i, d_y_i):
        self.x += d_x
        self.y += d_y
        self.x_i += d_x_i
        self.y_i += d_y_i
        if self.x > self.height:
            self.x -= self.height
            self.x_i -= self.size
        if self.y > self.height:
            self.y -= self.height
            self.y_i -= self.size



    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 255), (self.x, self.y), self.w)


class Logger(object):
    def __init__(self, screen, x, y):
        self.screen = screen
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.text_surface = self.font.render("Probabilities", False, (255, 255, 255))
        self.pos = (x,y)

    def draw_probs(self, probs):

        for i in range(len(probs)):
            text = ""
            for j in range(len(probs)):
                text += str(round(probs[i, j], 2)) + " "
            text_sur = self.font.render(text, False, (255, 255, 255))
            self.screen.blit(text_sur, (self.pos[0], self.pos[1]+(i+1)*18))

    def change_text(self, text):
        self.text_surface = self.font.render(text, False, (255, 255, 255))

    def draw(self):
        self.screen.blit(self.text_surface, self.pos)

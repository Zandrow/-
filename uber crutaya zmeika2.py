

import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("1/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("1/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # Движение тела за головой
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # Изменение направления движения
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Кто прочитал, тот поставит нам зачёт)")

        pygame.mixer.init()
        
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_sound(self, sound_name): # Звуки игры
        if sound_name == "crash":
            sound = pygame.mixer.Sound("1/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("1/ding.mp3")
        elif sound_name == 'scream':
            sound = pygame.mixer.Sound("1/scream.mp3")
        pygame.mixer.Sound.play(sound)

    def reset(self): # На случай рестарта
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2): # Условия коллизии
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self): # Фон
        bg = pygame.image.load("1/background.jpg")
        self.surface.blit(bg, (0,0))

    def render_background2(self): # Фон
        bg2 = pygame.image.load("1/background2.jpg")
        self.surface.blit(bg2, (0,0))

    def play(self): 
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Если змея ест яблоко
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # Если змея ест себя
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
        # Если змея ест стену
        for i in range(0, 801):
            if self.is_collision(self.snake.x[0], self.snake.y[0], -40, i):
                self.play_sound('crash')
                raise "Collision Occurred"
        for i in range(0, 801):
            if self.is_collision(self.snake.x[0], self.snake.y[0], 1000, i):
                self.play_sound('crash')
                raise "Collision Occurred"
        for i in range(0, 1001):
            if self.is_collision(self.snake.x[0], self.snake.y[0], i, -40):
                self.play_sound('crash')
                raise "Collision Occurred"
        for i in range(0, 1001):
            if self.is_collision(self.snake.x[0], self.snake.y[0], i, 800):
                self.play_sound('crash')
                raise "Collision Occurred"
    # Счётчик яблок
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Яблок съедено: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(750,10))

        if score == 100:
            raise ValueError("Game won")
    # На случай поражения
    def show_game_over(self):
        self.render_background2()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Ты проиграл! Твой счёт: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Для новой игры нажми ENTER. Чтобы выйти нажми ESC!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        self.play_sound("scream")
        pygame.display.flip()
    # На случай победы(требует доработки)
    def show_game_won(self): 
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render("Поздравляю! Ты победитель!", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Для новой игры нажми ENTER. Чтобы выйти нажми ESC!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
    # Передвижение
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()
            
            except ValueError as e:
                self.show_game_won()
                pause = True
                self.reset()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.15)

if __name__ == '__main__':
    game = Game()
    game.run()
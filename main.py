import pygame
import time
import random
from pygame.locals import *

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("apple_snake_game.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*5
        self.y = SIZE*5

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = SIZE*random.randint(0, 16)
        self.y = SIZE*random.randint(2, 14)


class Snake:
    def __init__(self, surface, length):
        self.parent_screen = surface
        self.length = length
        self.block = pygame.image.load("block_snake_game.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(40)
        self.y.append(40)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))  # draws the block on the game window

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE

        if self.direction == "down":
            self.y[0] += SIZE

        if self.direction == "left":
            self.x[0] -= SIZE

        if self.direction == "right":
            self.x[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()    # To initialize pygame
        pygame.mixer.init()   # To initialize music
        self.play_background_music()
        self.surface = pygame.display.set_mode((800, 600))
        self.render_background()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()

    def boundary_collision(self, x1, y1):
        if 0 <= x1 <= 800 and 0 <= y1 <= 600:
            return False
        return True

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True
        return False

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"{sound}")
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load("snake_background_music.mp3")
        pygame.mixer.music.play()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("Apple_eating.wav")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("Snake_collision.wav")
                raise "GAME OVER"

        # snake colliding with boundary
        if self.boundary_collision(self.snake.x[0], self.snake.y[0]):
            self.play_sound("Snake_collision.wav")
            raise "GAME OVER"

    def render_background(self):
        bg = pygame.image.load("background_snake_game.jpg")
        self.surface.blit(bg, (0, 0))

    def show_game_over(self):
        self.render_background()
        pygame.mixer.music.pause()
        font1 = pygame.font.SysFont("arial", 40)
        line1 = font1.render(f"GAME OVER! Your Score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (90, 200))
        font2 = pygame.font.SysFont("arial", 30)
        line2 = font2.render("To play again press Return. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (50, 250))
        pygame.display.flip()

    def reset(self):
        self.apple = Apple(self.surface)
        self.snake = Snake(self.surface, 1)

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"SCORE : {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (600, 10))

    def run(self):

        run = True
        pause = False

        while run:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()

                    if event.key == K_ESCAPE:
                        run = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    run = False

            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)


if __name__ == "__main__":
    game = Game()
    game.run()

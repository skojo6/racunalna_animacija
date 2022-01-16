import pygame
import random
import time


size = 20  # size of rectangles that snake/fruits consists of


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.length = 4  # starting length of the snake
        self.starting_snake_position = 360  # starting coordinates of snake/random number
                                            # to append for making snake bigger
        self.x = [self.starting_snake_position]*self.length  # starting x-axis coordinate of the snake
        self.y = [self.starting_snake_position]*self.length  # starting y-axis coordinate of the snake
        self.color = (0, 0, 0)  # snake color
        self.direction = 'up'  # starting direction of the snake
        self.step = 20  # step when snake changes direction
        self.score = 0  # how many fruits eaten

    # drawing snake on the screen
    def draw(self):
        for i in range(self.length):
            pygame.draw.rect(self.parent_screen, self.color, pygame.Rect(self.x[i], self.y[i], size, size))

    # changing direction of the snake to left
    def move_left(self):
        if self.direction == 'right':
            return
        self.direction = 'left'

    # changing direction of the snake to up
    def move_up(self):
        if self.direction == 'down':
            return
        self.direction = 'up'

    # changing direction of the snake to right
    def move_right(self):
        if self.direction == 'left':
            return
        self.direction = 'right'

    # changing direction of the snake to down
    def move_down(self):
        if self.direction == 'up':
            return
        self.direction = 'down'

    # lets snake move on its own
    def move(self):
        # while moving, all rectangles move to the place of their predecessor
        temp = [self.x[0], self.y[0]]
        for i in range(1, self.length):
            temp2 = [self.x[i], self.y[i]]
            self.x[i] = temp[0]
            self.y[i] = temp[1]
            temp = temp2

        # direction changes only for the 'head'
        if self.direction == 'left':
            self.x[0] -= self.step
        if self.direction == 'up':
            self.y[0] -= self.step
        if self.direction == 'right':
            self.x[0] += self.step
        if self.direction == 'down':
            self.y[0] += self.step

        # draw snake
        self.draw()

    # making snake bigger when it its fruit
    def eaten(self):
        self.score += 1
        self.length += 1
        self.x.append(self.starting_snake_position)
        self.y.append(self.starting_snake_position)


class Fruit:
    def __init__(self, parent_screen, parent_screen_size):
        self.parent_screen = parent_screen
        self.parent_screen_size = parent_screen_size
        self.x = random.randrange(0, parent_screen_size[0], size)  # starting x-axis coordinate of a fruit
        self.y = random.randrange(40, parent_screen_size[1], size)  # starting y-axis coordinate of a fruit
        self.color = (255, 255, 0)  # fruit color

    # draw fruit on the screen
    def draw(self):
        pygame.draw.rect(self.parent_screen, self.color, pygame.Rect(self.x, self.y, size, size))

    # creating new fruit when snake eats
    def eaten(self):
        self.x = random.randrange(0, self.parent_screen_size[0], size)
        self.y = random.randrange(40, self.parent_screen_size[1], size)


def show_final_score(screen_size, screen, score):
    time.sleep(1)  # sleep to see what stopped the game

    # defining fonts
    font = pygame.font.SysFont(None, 40)
    font2 = pygame.font.SysFont(None, 80)

    screen.fill(background_color)  # filling screen with background color

    # writing 'GAME OVER!' on screen
    game_over = font2.render("GAME OVER!", True, (255, 255, 255))
    gameover_rect = game_over.get_rect(center=(screen_size[0]/2, screen_size[1]/4))
    screen.blit(game_over, gameover_rect)

    # writing final score on screen
    score_init = font.render("FINAL SCORE: " + str(score), True, (255, 255, 255))
    score_rect = score_init.get_rect(center=(screen_size[0]/2, screen_size[1]/2))
    screen.blit(score_init, score_rect)

    pygame.display.update()

    time.sleep(5)  # sleep to see what the final score is
    pygame.quit()  # quiting the game
    return


def show_score(screen_size, screen, score):
    font = pygame.font.SysFont(None, 40)
    score_init = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_init, (5, 5))

    pygame.draw.line(screen, (255, 255, 255), (0, size*2), (screen_size[0], size*2))


if __name__ == "__main__":
    pygame.init()

    screen_size = (700, 700)  # size of the screen (tuple)
    background_color = (0, 128, 128)  # background color of the screen (RGB)
    screen_caption = 'SNAKE'  # caption of a window

    screen = pygame.display.set_mode(screen_size)  # setting screen size
    pygame.display.set_caption(screen_caption)  # setting caption of window
    screen.fill(background_color)  # filling screen with background color
    pygame.display.update()

    running = True  # flag for running/stopping program

    snake = Snake(screen)
    fruit = Fruit(screen, screen_size)

    while running:
        screen.fill(background_color)  # restarting screen for every move
        show_score(screen_size, screen, snake.score)

        # moving snake when pressing arrow keys
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    snake.move_left()
                if event.key == pygame.K_UP:
                    snake.move_up()
                if event.key == pygame.K_RIGHT:
                    snake.move_right()
                if event.key == pygame.K_DOWN:
                    snake.move_down()

        # snake movement
        snake.move()

        # drawing fruit
        fruit.draw()

        # eating fruit logic
        if snake.x[0] == fruit.x and snake.y[0] == fruit.y:
            snake.eaten()
            fruit.eaten()

        # wall collision logic
        if snake.x[0] == -size or snake.y[0] == size\
                or snake.x[0] == screen_size[0]\
                or snake.y[0] == screen_size[1]:
            show_final_score(screen_size, screen, snake.score)

        # game over logic - if snake collides with itself
        for i in range(1, snake.length):
            if snake.x[0] == snake.x[i] and snake.y[0] == snake.y[i]:
                show_final_score(screen_size, screen, snake.score)

        # periods of snake movement
        time.sleep(0.15)

        pygame.display.update()

import pygame
from pygame.locals import *
import random
import time
import os

#Apple, to create and position the apple in the game

class Apple():

    def __init__(self):
        self.apple = pygame.Surface((10, 10))
        self.apple.fill((255, 0, 0))
        self.position = (0, 0)

    def set_random_position(self, screen_size):
        self.position = (random.randrange(0, screen_size - 10, 10), random.randrange(40, screen_size - 10, 10))



UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

#Snake class: manages snake movement, collisions, and growth
class Snake():

    def __init__(self):
        self.snake = [(200, 200), (210, 200), (220, 200), (230, 200), (240, 200)]
        self.skin = pygame.Surface((10, 10))
        self.skin.fill((255, 255, 255))
        self.head = pygame.Surface((10, 10))
        self.head.fill((180, 180, 180))
        self.direction = None

    def crawl(self):
        if self.direction == None:
            return
        elif self.direction == RIGHT:
            self.snake.append((self.snake[len(self.snake) - 1][0] + 10, self.snake[len(self.snake) - 1][1]))
        elif self.direction == UP:
            self.snake.append((self.snake[len(self.snake) - 1][0], self.snake[len(self.snake) - 1][1] - 10))
        elif self.direction == DOWN:
            self.snake.append((self.snake[len(self.snake) - 1][0], self.snake[len(self.snake) - 1][1] + 10))
        elif self.direction == LEFT:
            self.snake.append((self.snake[len(self.snake) - 1][0] - 10, self.snake[len(self.snake) - 1][1]))
        self.snake.pop(0) #remover the tail to simulate movement

    def self_collision(self):
        return self.snake[-1] in self.snake[0:-1] #check if the snake hits itself

    def wall_collision(self, screen_size):
        #check if the snake hits the walls
        return self.snake[len(self.snake) - 1][0] >= screen_size or self.snake[len(self.snake) - 1][0] < 0 or \
            self.snake[len(self.snake) - 1][1] >= screen_size or self.snake[len(self.snake) - 1][1] < 40

    def snake_eat_apple(self, apple_pos): #check if the snake head is on the apple
        return self.snake[-1] == apple_pos

    def snake_bigger(self):
        self.snake.insert(0, (self.snake[0])) #add a new block to snake

#Score class
class Score():
    def __init__(self):
        self.score = 0
        self.score_text = pygame.font.Font(None, 25)

#Read the max score from a file
def read_max_score():
    if os.path.exists("max_score.txt"):
        with open("max_score.txt", "r") as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    return 0
#Save the max score to a file
def save_max_score(score):
    with open("max_score.txt", "w") as file2:
        file2.write(str(score))

#Music classes: background, food sound, loss sound
class Music():
    def __init__(self):
        self.music_load = pygame.mixer.music.load("background_sound.mp3")
        self.music_play = pygame.mixer.music.play(-1, 0.0)

class Food_Music():
    def __init__(self):
        self.food_music_load = pygame.mixer.Sound("level_up.wav")
        self.food_music_play = pygame.mixer.Sound("level_up.wav").play

class Loss_Music():
    def __init__(self):
        self.loss_music_load = pygame.mixer.Sound("lose.wav")
        self.loss_music_play = pygame.mixer.Sound("lose.wav").play


 #Game settings

GAME_ON = True
SPEED = 10
PAUSED = False
pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

#Display the intro screen before the game starts
def display_intro_screen():
    screen.fill((0, 0, 0))
    snake_foto = pygame.image.load("snake_game_foto.PNG")
    screen.blit(snake_foto, (0, 0))
    pygame.display.update()

    #wait for until the user press any key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                waiting = False
#Initalize game objects
snake = Snake()
apple = Apple()
score = Score()
music = Music()
food_music = Food_Music()
loss_music = Loss_Music()
apple.set_random_position(500)
pygame.display.set_caption("Snake Game")
max_score = read_max_score()
max_score_text = pygame.font.Font(None, 25)

#Sound Settings
MUSIC_ON = True
sound_icon = pygame.image.load("medium-volume.png")
mute_icon = pygame.image.load("mute.png")
sound_font = pygame.font.Font(None, 36)  

display_intro_screen()

#Main game loop
while GAME_ON:

    clock.tick(SPEED)

    for event in pygame.event.get():
        if event.type == QUIT:
            GAME_ON = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                GAME_ON = False
            elif event.key == K_p:
                PAUSED = not PAUSED


            #Control snake direction and music toggling
            if not PAUSED:
                if event.key == K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key == K_m:
                    if MUSIC_ON:
                        pygame.mixer.music.stop()

                    else:
                        pygame.mixer.music.play()
                    MUSIC_ON = not MUSIC_ON  


    if not PAUSED: 
        snake.crawl() #move the snaje
        pygame.mixer.music.unpause()



        #Check for collisions or eating the apple
        if snake.wall_collision(500) or snake.self_collision():
            pygame.mixer.music.stop()
            loss_music.loss_music_play()
            time.sleep(1)
            GAME_ON = False


        if snake.snake_eat_apple(apple.position):
            apple.set_random_position(500)
            snake.snake_bigger()
            SPEED = min(SPEED + 0.2, 30)
            score.score += 1
            food_music.food_music_play()

        #Update max score if the current score exceeds it
        if score.score > max_score:
            max_score = score.score
            save_max_score(max_score)

        #Redraw game elements
        screen.fill((0, 0, 0))

        for snake_pos in snake.snake[0:-1]:
            screen.blit(snake.skin, snake_pos)
        score_font = score.score_text.render(f"SCORE: {score.score}", True, (255,255,255))
        max_score_font = max_score_text.render(f"Max Score: {max_score}", True, (255,255,255))
        screen.blit(snake.head, snake.snake[-1])
        screen.blit(apple.apple, apple.position)
        screen.blit(score_font, (10,10))
        screen.blit(max_score_font, (150,10))
        pygame.draw.line(screen, (255,255,255),(0,38),(500,38), 3)

        #Display sound icon
        if MUSIC_ON:
            screen.blit(sound_icon, (450,5))
        else:
            screen.blit(mute_icon, (450,5))
    else:
        #Display pause screen
        screen.fill((0, 0, 0))
        paused_foto = pygame.image.load("paused_foto.png")
        screen.blit(paused_foto, (0, 0))
        pygame.display.update()
        pygame.mixer.music.pause()



    pygame.display.update()

#Game over screen
screen.fill((0,0,0))
game_over = pygame.image.load("game_over_foto.png")
screen.blit(game_over,(0,0))
pygame.display.update()
time.sleep(2)
pygame.quit()
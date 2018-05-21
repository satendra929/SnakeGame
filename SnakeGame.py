import pygame
import sys
from random import randint

#Right -- R
#Left -- L
#Up -- U
#Down -- D


#File to write scores
file = open("scores.txt","r+")
str_scores = file.readlines()
if len(str_scores) == 0:
    H_SCORE = 0
else:
    H_SCORE = max(list(map(int,str_scores)))
STR_MSG = "GAME OVER"

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GRAY = (128,128,128)
SPEED = 3
SCORE = 0
GAME_OVER = False
(width, height) = (400, 400)
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
fps = pygame.time.Clock()
screen.fill(BLACK)
#setup font
myfont = pygame.font.SysFont('monospace', 30)
text = myfont.render(STR_MSG, True, WHITE)
pygame.display.update()

class Snake() :
    global screen
    def __init__(self):
        self.head_position = [200,200]
        self.body = [[200,200],[210,200],[220,100]]
        self.direction = "L"
        self.draw_snake()

    def draw_snake(self):
        for index, value in enumerate(self.body):
            if (index == 0):
                pygame.draw.circle(screen, WHITE, value, 5)
            else:
                pygame.draw.circle(screen, GRAY, value, 5)
        pygame.display.update()

    def position_update(self):
        if (self.direction == "R") :
            self.head_position[0] = self.head_position[0] + 10
            self.body = [list(self.head_position)] + self.body[:-1]
        elif (self.direction == "L") :
            self.head_position[0] = self.head_position[0] - 10
            self.body = [list(self.head_position)] + self.body[:-1]
        elif (self.direction == "U") :
            self.head_position[1] = self.head_position[1] - 10
            self.body = [list(self.head_position)] + self.body[:-1]
        elif (self.direction == "D") :
            self.head_position[1] = self.head_position[1] + 10
            self.body = [list(self.head_position)] + self.body[:-1]
        self.draw_snake()

    def change_direction(self,direc):
        if ( direc == "L" and self.direction != "R"):
            self.direction = direc
        elif ( direc == "R" and self.direction != "L"):
            self.direction = direc
        elif ( direc == "U" and self.direction != "D"):
            self.direction = direc
        elif ( direc == "D" and self.direction != "U"):
            self.direction = direc

    def check_collisions(self):
        if not all((cor >= 5 and cor <= 395) for cor in self.head_position):
            screen.blit(text,(100,200))
            pygame.display.update()
            return True
        if self.head_position in self.body[1:]:
            screen.blit(text,(100,200))
            pygame.display.update()
            return True

    def game_over(self):
        file.close()
        pygame.quit()
        sys.exit()

class Rat_Spawner():
    def __init__(self):
        self.position = [randint(1,39)*10,randint(1,39)*10]
        self.presence = True
        self.draw_rat()

    def spawn(self):
        if self.presence == False:
            self.position = [randint(1,39)*10,randint(1,39)*10]
            self.presence = True
            self.draw_rat()
            
    def draw_rat(self):
        pygame.draw.circle(screen, RED, self.position, 5)

#main
snake_object = Snake()
rs = Rat_Spawner()
while True :
    if GAME_OVER == False:
        if snake_object.head_position == rs.position:
            addition = [snake_object.body[-1][0] - 10,snake_object.body[-1][1]]
            snake_object.body.append(addition)
            rs.presence = False
            rs.spawn()
            SCORE += 10
            SPEED+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake_object.game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake_object.change_direction("R")
                elif event.key == pygame.K_LEFT:
                    snake_object.change_direction("L")
                elif event.key == pygame.K_UP:
                    snake_object.change_direction("U")
                elif event.key == pygame.K_DOWN:
                    snake_object.change_direction("D")
        screen.fill(BLACK)
        rs.draw_rat()
        snake_object.position_update()
        if snake_object.check_collisions():
            file.write((str)(SCORE))
            if SCORE > H_SCORE :
                STR_MSG = "YEAH ! HIGHSCORE :)"
            GAME_OVER = True
            SPEED = 27
    else :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake_object.game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:          
                    GAME_OVER = False
                    SCORE = 0
                    SPEED = 3
                    STR_MSG = "GAME OVER"
                    snake_object.head_position = [200,200]
                    snake_object.body = [[200,200],[210,200],[220,100]]
    pygame.display.set_caption("Snake | SCORE: "+(str)(SCORE))
    fps.tick(SPEED)
            

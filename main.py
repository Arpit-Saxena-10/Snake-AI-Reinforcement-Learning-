import pygame
import numpy
import random


pygame.init()

"""
# setting up the screen
screen = pygame.display.set_mode((240,240))

# Title and Logo
pygame.display.set_caption("This is the Title")
"""

FOOD_IMG = 'apple_24'
SQUARE_IMG = 'Square_24'
IMG_SIZE = 24
LEN = 10

class food():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = FOOD_IMG



class square():                                 #square represents a single unit of the snake body
    def __init__(self,x,y,direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.img = SQUARE_IMG
        self.kill = False

    def update_pos(self):
        if self.direction == 0:
            self.y += -IMG_SIZE
        elif self.direction == 1:
            self.x += IMG_SIZE
        elif self.direction == 2:
            self.y += IMG_SIZE
        if self.direction == 3:
            self.x += -IMG_SIZE

    def set_direction(self,direction):
        self.direction = direction

class snake():
    def __init__(self,x,y,direction):
        self.head = square(x,y,direction)
        self.length = 1
        self.body = [self.head]
        self.collision_position = []
        self.collision_direction = []
        self.state = 0             #state will be set to 1 when snake's length has to be increased by 1 square
        self.kill = 0

    def move(self):
        for square in self.body:
            square.update_pos()
        if self.state == 1:
            self.add_square()


    def update_direction(self,direction):
        for i in reversed(range(len(self.body))):
            if i >= 1:
                self.body[i].set_direction(self.body[i-1].direction)
            elif i == 0:
                self.body[i].set_direction(direction)

    def check_food(self,food):
        if self.body[0].x == food.x and self.body[0].y == food.y:
            self.collision_position.append([self.body[0].x,self.body[0].y])
            self.collision_direction.append([self.body[0].direction])
            return True
        else:
            return False
    def add_square(self):
        new_square = square(self.collision_position[len(self.collision_position) - 1][0],
                            self.collision_position[len(self.collision_position) - 1][1],
                            self.collision_direction[len(self.collision_direction) - 1])
        self.body.append(new_square)
        self.collision_position.pop()
        self.collision_direction.pop()
        self.state = 0


    def check_extension(self):
        if len(self.collision_position)>0:
            if self.body[len(self.body)-1].x == self.collision_position[len(self.collision_position)-1][0] and self.body[len(self.body)-1].y == self.collision_position[len(self.collision_position)-1][1]:
                self.state = 1

    def check_trip(self):
        for i in range(len(self.body)):
            if i>0:
                if self.body[0].x == self.body[i].x and self.body[0].y == self.body[i].y:
                    return True
        return False

    def check_wall(self):
        if self.body[0].x <-1 or self.body[0].x >((LEN-1)*IMG_SIZE+1) or self.body[0].y <-1 or self.body[0].y >((LEN-1)*IMG_SIZE+1):
            return True
        else:
            return False

    def check_death(self):
        return self.check_trip() or self.check_wall()


def adjacent_squares(snake,food):                               #will contain information about whats on squares adjacent to the head of snake
    squares = [1,1,1,1]                                         #0th index - up, index 1 - right, index 2 - down, index 3 - left
    head = [snake.body[0].x,snake.body[0].y]                    #0 - wall or snake body, 1 - empty space , 2 - food

    #checking for food adjacent to the head of the snake

    if (head[0]-1) == food.x and head[1] == food.y:
        squares[3] = 2
    if (head[0] + 1) == food.x and head[1] == food.y:
        squares[1] = 2
    if head[0] == food.x and (head[1]-1) == food.y:
        squares[0] = 2
    if head[0] == food.x and (head[1]+1) == food.y:
        squares[2] = 2

    # checking for wall
    if (head[0]-1) < -1:
        squares[3] = 0
    if (head[0]+1) >= ((LEN-1)*IMG_SIZE+1):
        squares[3] = 0
    if (head[1]-1) < -1:
        squares[3] = 0
    if (head[0]+1) >= ((LEN-1)*IMG_SIZE+1):
        squares[3] = 0

    #checking for snake body
    for i in range(len(snake.body)):
        if i > 0:
            if (head[0] - 1) == snake.body[i].x and head[1] == snake.body[i].y:
                squares[3] = 0
            if (head[0] + 1) == snake.body[i].x and head[1] == snake.body[i].y:
                squares[1] = 0
            if  head[0] == snake.body[i].x and (head[1] - 1) == snake.body[i].y:
                squares[0] = 0
            if  head[0] == snake.body[i].x and (head[1]+1) == snake.body[i].y:
                squares[2] = 0
    squares_tuple = (squares[0],squares[1],squares[2],squares[3])

    return squares
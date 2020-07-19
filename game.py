import pygame
import numpy
import random
from main import square,snake,food,adjacent_squares
from RL_agent import state,rl_agent,q_table,update_qtable
import pickle
import time

FOOD_IMG = 'apple_24.png'
SQUARE_IMG = 'Square_24.png'


# initiallizing pygame so we can use it
pygame.init()

# setting up the screen
screen = pygame.display.set_mode((240, 240))

# Title and Logo
pygame.display.set_caption("This is the Title")


def random_no():
    return 24*random.randint(0,9)

def render_food(food):
    img = pygame.image.load(FOOD_IMG)
    screen.blit(img,(food.x,food.y))

def render_snake(snake):
    img = pygame.image.load(SQUARE_IMG)
    for square in snake.body:
        screen.blit(img,(square.x,square.y))




q_file = open("q_table_trained_210,000.pkl", "rb")
q_table = pickle.load(q_file)


direc = 0
MAX_EPISODES = 100
episode = 0
score_track = []
MAX_EPSILON = 0
LEARNING_RATE = 0.15
# Game Loop
def state(snake,food):
    relative_x = snake.body[0].x - food.x
    relative_y = snake.body[0].y - food.y


    adjacent  = adjacent_squares(snake,food)

    return (relative_x,relative_y,adjacent[0],adjacent[1],adjacent[2],adjacent[3])


while episode < MAX_EPISODES:
    run = True

    action = 0
    direc = 0
    reward = -2
    count = 0
    score = 0

    apple = food(random_no(), random_no())
    player = snake(96,96,0)

    old_state = state(player, apple)

    while run:
        count += 1
        screen.fill((220, 220, 220))
        new_state = state(player,apple)

        update_qtable(old_state,new_state,action,LEARNING_RATE,0.95,reward,q_table)
        reward = -2
        old_state = state(player,apple)
        epsilon = MAX_EPSILON*(1-(episode/(0.95*MAX_EPISODES))**5)
        action = rl_agent(new_state,epsilon,q_table)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if episode> 0.99*MAX_EPISODES:
            render_food(apple)
            render_snake(player)
            time.sleep(0.09)
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direc = 3
            if event.key == pygame.K_RIGHT:
                direc = 1
            if event.key == pygame.K_UP:
                direc = 0
            if event.key == pygame.K_DOWN:
                direc = 2
        """
        direc = action

        if count%128 >-1:
            player.update_direction(direc)
            player.move()

            if player.check_food(apple):
                apple = food(random_no(),random_no())
                reward = 400
                score+=1
            player.check_extension()



        if player.check_death() == True:
            reward = -1_000
            player.kill = True
            score_track.append(score)
        if player.kill == True:
            player = snake(96,96,0)
            run = False
        pygame.display.update()
    episode+=1

print(sum(score_track)/len(score_track))
print(max(score_track))
print(score_track[-100:])


#q_file = open("2nd_q_table_trained_210,000.pkl", "wb")
#pickle.dump(q_table, q_file)
q_file.close()

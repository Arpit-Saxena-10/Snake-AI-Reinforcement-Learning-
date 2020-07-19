import numpy
import pygame
import random
from main import snake,square,food,adjacent_squares,LEN
import pickle





q_table = {}
relative_range = list(range(2*LEN-1))
for i in range(len(relative_range)):
    relative_range[i] = (relative_range[i]-(LEN-1))*24

def arg_index(arr):
    max_index = 0
    max_so_far = arr[0]
    for i in range(len(arr)):
        if arr[i] > max_so_far:
            max_index = i
            max_so_far = arr[i]
    return max_index

# to make random q_table
for x in relative_range:
    for y in relative_range:
        for left in range(3):
            for right in range(3):
                for up in range(3):
                    for down in range(3):
                        state = (x,y,up,right,down,left)
                        q_table[state] = [random.random(),random.random(),random.random(),random.random()]

def update_qtable(old_state,new_state,action,learning_rate,discount,reward,q_table):

    q_value = q_table[old_state][action]

    q_table[old_state][action] = (1-learning_rate)*q_value + learning_rate*(reward + discount*max(q_table[new_state]))

def rl_agent(state,epsilon,q_table):

    if random.random() < epsilon:
        action = random.randint(0,3)
    else:
        #if q_table.has_key(state):
        action = arg_index(q_table[state])
        #else:
        #    action = random.randint(0,3)

    return action

dictionary_data = {"a": 1, "b": 2}

q_file = open("q_table.pkl", "wb")
pickle.dump(q_table, q_file)
q_file.close()
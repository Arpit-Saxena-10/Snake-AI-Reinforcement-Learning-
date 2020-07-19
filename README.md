# Snake-AI-Reinforcement-Learning-
This project aims to make a Reinforcement Learning AI bot that can play the popular Snake game.Currently, I'm using the Q-Learning method to train the AI, more details are given below

State : Relative position of the snake head and food, information on what is present in the squares adjacent to the snake head (in a tuple)
Reward : +400 -> on getting food
         -500 -> on hitting the edge or itself 
          -12 -> rest 

As the State does not contain enough information, the AI won't be able to play optimally.In the future I would like to update the training method from Q-Learning to Deep Q-Learning with the image of the game as the state(so the AI has full info about the situation).

How Good is this AI?
With a training of about 50,000 games, it scores about 4.6 food on average and can go as high as 18 if it gets lucky.Obviously, there is still room for improvement.

![Alt Text](https://github.com/Arpit-Saxena-10/Snake-AI-Reinforcement-Learning-/blob/master/9.gif)

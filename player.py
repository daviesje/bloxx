# -*- coding: utf-8 -*-
"""
Created on Sat May 18 22:34:32 2019

@author: jed12
"""
import objects
from NeuralNet import network

xspeed = 5

class Player():
    def __init__(self):
        self.net = network.Network()
        self.net.fresh_start()
        self.net.mutate()
        self.score = 0
        self.jumping = False
        self.fallen = False
        self.x_pos = objects.x_init
        self.y_pos = objects.player_floor_1
        self.x_vel = xspeed
        self.y_vel = 0
        self.angle = 0
        self.win = False
        self.dead = False
        self.image = 4
        self.crashes = 0
        
class Human():
    def __init__(self):
        self.score = 0
        self.jumping = False
        self.fallen = False
        self.x_pos = objects.x_init
        self.y_pos = objects.player_floor_1
        self.x_vel = xspeed
        self.y_vel = 0
        self.angle = 0
        self.win = False
        self.dead = False
        self.image = 0
        self.crashes = 0
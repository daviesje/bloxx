# -*- coding: utf-8 -*-
import pygame
import sys
from numpy.random import randint,choice

cur_level = None
cur_level_n = 0

GRID_SIZE = 32 #cell size in pixels
box_width = 32
box_height = 32

class level():
    def __init__(self):
        self.nobs = 0
        self.obsx = []
        self.obsarr = []
        self.boxim = []
        self.obsfloor = []
    def add_obstacle(self,obs,x,floor):
        self.nobs = self.nobs + 1
        self.obsx.append(x)
        self.obsarr.append(obs)
        self.boxim.append(2)
        #TODO: image dimensions for tiling (when you draw more)
        self.obsfloor.append(floor)
    
#future stuff, deprecated
class alt_level():
    def __init__(self):
        self.altboxx = []
        self.altboxy = []
        self.altboxw = []
        self.altboxh = []
        self.altboxim = []
        self.altboxc = []
        self.altboxfloor = []
    def add_switch(self,x,y,floor,boxdel,boxadd):
        self.nswitch = self.nswitch + 1
        self.switchx.append(x)
        self.switchy.append(y)
        self.switchfloor.append(floor)
        self.switchdel.append(boxdel)
        self.switchadd.append(boxadd)
    def add_altbox(self,x,y,floor):
        self.altboxx.append(x)
        self.altboxy.append(y)
        self.altboxw.append(32)
        self.altboxh.append(32)
        self.altboxim.append(2)
        self.altboxfloor.append(floor)

class Obstacle():
    def __init__(self,w,h,c,o,sb,sa,d):
        self.width = w
        self.height = h
        self.ceil = c
        self.offset = o
        self.spacebefore = sb
        self.spaceafter = sa
        self.diff = d

#defining types of obstacle here
smallJump = Obstacle(1,1,5,0,1,1,0)
twoJump = Obstacle(1,2,5,0,1,1,0)
box = Obstacle(2,2,5,0,2,2,0)
noJump = Obstacle(1,0,1,0,1,1,0)
highJump = Obstacle(1,3,5,0,2,2,1)
longJump = Obstacle(3,1,5,0,1,1,1)
earlyJump_1 = Obstacle(1,1,4,3,4,2,2)
lateJump_1 = Obstacle(1,1,4,-3,2,4,2)
biggun_h = Obstacle(3,2,5,0,2,2,3)
biggun_v = Obstacle(2,3,5,0,2,2,3)
earlyJump_2 = Obstacle(1,2,3,3,4,2,4)
lateJump_2 = Obstacle(1,2,3,-3,2,4,4)
gap1 = Obstacle(1,1,4,0,2,2,5) #maybe get rid of this
tunnel = Obstacle(5,0,1,0,1,1,5)
lateJump_3 = Obstacle(3,2,2,-4,2,4,6) #maybe get rid of this
earlyJump_3 = Obstacle(3,2,2,4,2,4,6) #maybe get rid of this
end = Obstacle(2,4,5,0,1,1,10)
obslist = [smallJump,noJump,box
           ,highJump,longJump
           ,earlyJump_1,lateJump_1
           ,biggun_h,biggun_v
           ,earlyJump_2,lateJump_2
           ,tunnel
           ,lateJump_3,earlyJump_3
           ,end]

#obslist = [noJump,earlyJump_2,lateJump_2]


level1 = level()
#levelarr = [level1]
levelarr = []
num_levels = len(levelarr)

for i,lev in enumerate(levelarr):
    filename = f'levels/level{i+1}.txt'
    with open(filename) as file:
        for line in file:
            line = line.strip('\n')
            linearr = line.split('\t')
            linearr[1] = int(linearr[1])
            linearr[2] = int(linearr[2])
            if linearr[0] == 'smalljump':
                lev.add_obstacle(smallJump,linearr[1],linearr[2])
            if linearr[0] == 'nojump':
                lev.add_obstacle(noJump,linearr[1],linearr[2])
            if linearr[0] == 'highjump':
                lev.add_obstacle(highJump,linearr[1],linearr[2])
            if linearr[0] == 'longjump':
                lev.add_obstacle(longJump,linearr[1],linearr[2])
            if linearr[0] == 'earlyjump':
                lev.add_obstacle(earlyJump,linearr[1],linearr[2])
            if linearr[0] == 'latejump':
                lev.add_obstacle(lateJump,linearr[1],linearr[2])

def generate_level(lnum):
    global obslist
    diff = lnum
    lev = level()

    #generate first floor
    space = 0
    last_x = 5
    last_w = 0
    min_edge = 0
    while min_edge <= 35:
        while True:
            obs = choice(obslist)
            spacebuf = obs.spacebefore + space            
            buffer = randint(0,3) + max(8-diff,0)
            obs_x = last_x + 1 + spacebuf + buffer + last_w
            obs_edge = obs_x + obs.width
            if obs.diff <= diff and obs_edge <= 35:
                break
        lev.add_obstacle(obs,obs_x,0)
        last_x = obs_x
        last_w = obs.width
        space = obs.spaceafter
        #if the last space was short, add a little more space to the next one
        if spacebuf + buffer <= 5:
            space += 5
        min_edge = last_x + last_w + space + 4 + max(7-diff,0)    
        #4 in min edge is min_space (2) + 1(const) + min_w(1)

    #generate second floor
    space = 0
    last_x = 32
    last_w = 0
    #care less about spacing here, objects off screen are A.O.K
    while last_x - space > 2:
        while True:
            obs = choice(obslist)
            spacebuf = obs.spacebefore + space
            #TODO: think of x~2 restrictions
            if obs.diff <= diff:
                break
        buffer = randint(0,3) + max(8-diff,0)
        obs_x = last_x - 1 - spacebuf - buffer - obs.width
        lev.add_obstacle(obs,obs_x,1)
        last_x = obs_x
        space = obs.spaceafter

    return lev

def next_level():
    global cur_level, cur_level_n
    cur_level_n += 1
    #print(f'next level = {cur_level} + 1 out of {num_levels}')
    if cur_level_n >= num_levels:
        cur_level = generate_level(cur_level_n)
        return True
    else:
        return False
        
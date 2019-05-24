# -*- coding: utf-8 -*-
import pygame
import sys
from numpy.random import randint

cur_level = 1

box_width = 32
box_height = 32

class level():
    def __init__(self):
        self.nbox = 0
        self.boxx = []
        self.boxy = []
        self.boxw = []
        self.boxh = []
        self.boxim = []
        self.boxfloor = []
        self.altboxx = []
        self.altboxy = []
        self.altboxw = []
        self.altboxh = []
        self.altboxim = []
        self.altboxfloor = []
        self.nswitch = 0
        self.switchx = []
        self.switchy = []
        self.switchfloor = []
        self.switchdel = []
        self.switchadd = []
    def add_box(self,x,y,floor):
        self.nbox = self.nbox + 1
        self.boxx.append(x*32.)
        self.boxy.append(y*32.)
        self.boxw.append(32)
        self.boxh.append(32)
        self.boxim.append(2)
        self.boxfloor.append(floor)
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

level1 = level()
level2 = level()
level3 = level()
level4 = level()
level5 = level()
levelarr = [level1,level2,level3,level4,level5]
num_levels = len(levelarr)

for i,lev in enumerate(levelarr):
    filename = f'levels/level{i+1}.txt'
    with open(filename) as file:
        for line in file:
            line = line.strip('\n')
            linearr = line.split('\t')
            linearr[1] = int(linearr[1])
            linearr[2] = int(linearr[2])
            linearr[3] = int(linearr[3])
            if linearr[0] == 'box':
                lev.add_box(linearr[1],linearr[2],linearr[3])
            if linearr[0] == 'switch':
                linearr[4] = linearr[4].split(',')
                if linearr[4] == ['']:
                    linearr[4] = []
                else:
                    linearr[4] = [int(ii) for ii in linearr[4]]
                linearr[5] = linearr[5].split(',')
                if linearr[5] == ['']:
                    linearr[5] = []
                else:
                    linearr[5] = [int(ii) for ii in linearr[5]]
                lev.add_switch(linearr[1],linearr[2],linearr[3],linearr[4],linearr[5])
            if linearr[0] == 'altbox':
                lev.add_altbox(linearr[1],linearr[2],linearr[3])
                
def generate_level(lnum):
    rnum = lnum - num_levels
    lev = level()
    min_jump = min(rnum + 2,8)
    max_jump = min(rnum + 5,8)
    min_dist = max(10 - rnum, 4)
    last_x = 0
    last_w = 0
    last_h = 0
    last_c = 0
    
    n_jump = randint(min_jump,max_jump+1)
    for ii in range(n_jump):
        #set x_dist
        x = last_x + last_w + randint(min_dist,10)
        w = randint(1,4)
        h = randint(1,5-w)
        c = randint(h+2,7)

        lev.add_box(0,h-1,0)
        lev.add_box(w,h-1,0)
        lev.add_box(0,c,0)
        lev.add_box(w,c,0)
 
    for ii in range(n_jump):
        #set x_dist
        x = last_x + last_w + randint(min_dist,10)
        w = randint(1,4)
        h = randint(1,5-w)
        c = randint(h+2,7)
        
        lev.add_box(0,h-1,1)
        lev.add_box(w,h-1,1)
        lev.add_box(0,c,1)
        lev.add_box(w,c,1)
        
    return lev

def next_level():
    global cur_level
    cur_level += 1
    #print(f'next level = {cur_level} + 1 out of {num_levels}')
    if cur_level > num_levels:
        return True
    else:
        return False
        
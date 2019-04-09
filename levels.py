# -*- coding: utf-8 -*-
import pygame
import sys

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
        self.boxx.append(x)
        self.boxy.append(y)
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
level1.add_box(320,0,0)
level1.add_box(640,0,0)
level1.add_box(960,32,0)
level1.add_box(800,0,1)
level1.add_box(800,32,1)
level1.add_box(800,64,1)
level1.add_box(480,16,1)

level2 = level()
level2.add_box(320,0,0)
level2.add_box(640,0,0)
level2.add_box(672,0,0)
level2.add_box(672,32,0)
level2.add_box(672,0,0)
level2.add_box(800,0,1)
level2.add_box(608,0,1)
level2.add_box(416,0,1)
level2.add_box(960,0,0)
level2.add_box(1024,96,0)

level3 = level()
level3.add_box(320,0,0)
level3.add_box(352,0,0)
level3.add_box(384,0,0)
level3.add_box(352,32,0)
level3.add_box(640,0,0)
level3.add_box(640,32,0)
level3.add_box(800,0,1)
level3.add_box(672,96,1)
level3.add_box(544,0,1)
level3.add_box(416,96,1)
level3.add_box(288,0,1)

level4 = level()
level4.add_box(160,0,0)
level4.add_box(192,0,0)
level4.add_box(224,0,0)
level4.add_box(640,0,0)
level4.add_box(640,32,0)
level4.add_box(640,64,0)
level4.add_box(640,96,0)
level4.add_switch(320,64,0,[5,6],[])
level4.add_box(1024,0,0)
level4.add_box(864,0,1)
level4.add_box(864,32,1)
level4.add_box(864,64,1)
level4.add_box(896,32,1)
level4.add_box(896,0,1)
level4.add_box(928,0,1)
level4.add_switch(640,96,1,[17,18],[0,1])
level4.add_box(416,0,1)
level4.add_box(384,0,1)
level4.add_box(352,0,1)
level4.add_box(320,0,1)
level4.add_box(288,0,1)
level4.add_altbox(160,0,1)
level4.add_altbox(192,0,1)

levelarr = [level1,level2,level3,level4]
num_levels = len(levelarr)

def next_level():
    global cur_level
    if cur_level == num_levels:
        end_win()
    else:
        cur_level = cur_level + 1
        level_win = True

def end_win():
    pygame.quit()
    sys.exit()
# -*- coding: utf-8 -*-
'''
Contains classes and functions for drawing and manipulating objects
'''
import pygame
import init
import levels

x_init = init.display_width*0.01
y_init = init.display_height*0.5

player_base = 16
player_height = 16
floor_height = 16
gap_width = 64
switch_width = 32
switch_height = 32
box_idx = []
switch_idx = []
altbox_idx = []

player_floor_1 = y_init - floor_height
player_floor_2 = init.display_height - 2*floor_height

def draw_player(x,y,angle):
    init.gameDisplay.blit(pygame.transform.rotate(init.Imlist.images[0],angle),(x,y))
    
def draw_floors():
    init.gameDisplay.blit(init.Imlist.images[1],(-gap_width,y_init))
    init.gameDisplay.blit(init.Imlist.images[1],(0,init.display_height - floor_height))
    
def draw_level(level):
    lev = levels.levelarr[level-1]

    for box in box_idx:
        init.gameDisplay.blit(init.Imlist.images[lev.boxim[box]]
                              ,(lev.boxx[box]
                              ,lev.boxfloor[box]*player_floor_2
                              + (1-lev.boxfloor[box])*player_floor_1
                              - lev.boxy[box] - floor_height))
        
    for box in altbox_idx:
        init.gameDisplay.blit(init.Imlist.images[lev.altboxim[box]]
                              ,(lev.altboxx[box]
                              ,lev.altboxfloor[box]*player_floor_2
                              + (1-lev.altboxfloor[box])*player_floor_1
                              - lev.altboxy[box] - floor_height))
    for switch in switch_idx:
        init.gameDisplay.blit(init.Imlist.images[3]
                              ,(lev.switchx[switch]
                              ,lev.switchfloor[switch]*player_floor_2
                              + (1-lev.switchfloor[switch])*player_floor_1
                              - lev.switchy[switch] - floor_height))
        
def test_collision(x,y,lnum):
    global box_idx, altbox_idx, switch_idx
    lev = levels.levelarr[lnum-1]
    for box in box_idx:
        box_y = lev.boxfloor[box]*player_floor_2
        box_y += (1-lev.boxfloor[box])*player_floor_1
        box_y += - lev.boxy[box] - floor_height
        x_lower = lev.boxx[box] - player_base
        x_upper = lev.boxx[box] + lev.boxw[box]
        y_lower = box_y + player_height
        y_upper = box_y - lev.boxh[box]
        
        if x>=x_lower and x<=x_upper and y<=y_lower and y>=y_upper:
            return True

    for box in altbox_idx:
        box_y = lev.altboxfloor[box]*player_floor_2
        box_y += (1-lev.altboxfloor[box])*player_floor_1
        box_y += - lev.altboxy[box] - floor_height
        x_lower = lev.altboxx[box] - player_base
        x_upper = lev.altboxx[box] + lev.altboxw[box]
        y_lower = box_y + player_height
        y_upper = box_y - lev.altboxh[box]
        
        if x>=x_lower and x<=x_upper and y<=y_lower and y>=y_upper:
            return True

    for switch in switch_idx:
        switch_y = lev.switchfloor[switch]*player_floor_2
        switch_y += (1-lev.switchfloor[switch])*player_floor_1
        switch_y += - lev.switchy[switch] - floor_height
        x_lower = lev.switchx[switch] - player_base
        x_upper = lev.switchx[switch] + switch_width
        y_lower = switch_y + player_height
        y_upper = switch_y - switch_width
        
        if x>=x_lower and x<=x_upper and y<=y_lower and y>=y_upper:
            for dd in lev.switchdel[switch]:
                box_idx.remove(dd)
            for aa in lev.switchadd[switch]:
                altbox_idx.append(aa)
            switch_idx.remove(switch)
                

    return False
# -*- coding: utf-8 -*-
'''
Contains classes and functions for drawing and manipulating objects
'''
import pygame
import init
import levels
import numpy as np

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

def draw_player(x,y,angle,image):
    #print(f'drawing payer at ({x},{y},{angle})')
    init.gameDisplay.blit(pygame.transform.rotate(init.Imlist.images[image],angle),(x,y))
    
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

def draw_net(net):
    screencen = init.display_width/2.
    netcen = int(net.layers/2)
    nhist = [0]*net.layers
    num_in_layer = []
    for n in net.nodeList:
        nhist[n.layer] += 1
        num_in_layer.append(nhist[n.layer])
    max_nodes = max(nhist)

    nodex = []
    nodey = []
    offset = [0,-4,4,-2,2,0]

    for ii,node in enumerate(net.nodeList):
        nodex.append(int(screencen + (node.layer - netcen)*64))
        nodey.append(int(16*num_in_layer[ii]*max_nodes/(nhist[node.layer] + 1)
        + offset[node.layer]))
        pygame.draw.circle(init.gameDisplay,(0,0,0),(nodex[ii],nodey[ii]),4)
    for ii,conn in enumerate(net.connectionList):
        green = min(max([0,conn.weight])*64,255)
        red = min(-min([0,conn.weight])*64,255)
        pygame.draw.line(init.gameDisplay,(red,green,0),(nodex[conn.fromNode.nodeNo],
                         nodey[conn.fromNode.nodeNo]),(nodex[conn.toNode.nodeNo],
                         nodey[conn.toNode.nodeNo]),abs(int(2*conn.weight)) + 1)
        
def test_collision(x,y,lnum):
    global box_idx
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

def test_altcollision(x,y,lnum):
    global altbox_idx, switch_idx
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

#TODO: SWITCHES / ALTBOXES
def look(x,y,f,lnum):
    global box_idx
    lev = levels.levelarr[lnum-1]
    xdist = np.array(lev.boxx)
    floor = np.array(lev.boxfloor)
    xdist = xdist - x
    #bottom floor goes backwards
    if f == 1:
        xdist = -xdist
    sel = np.logical_and(xdist>0,floor==f)
    #get rid of wrong floor and past boxes
    xdist = xdist[sel]
    ydist = np.array(lev.boxy)[sel]
    #order by x distance then y distance ()
    idx = np.argsort(xdist + ydist/1200)
    #xlen = np.array(lev.boxw)
    #ylen = np.array(lev.boxh)
    bias = 1
    l1,l2,l3,l4,l5,l6,l7,l8,l9,la = 100,0,0,0,100,0,100,0,100,0
    if len(idx) >= 1:
        l1 = xdist[idx[0]]/32                   #x dist to next box
        l2 = ydist[idx[0]]/32                #y dist to next box
        #l3 = xlen[idx[0]]/32                #next box width
        #l4 = ylen[idx[0]]/32                #next box height
        if len(idx) >= 2:
            l5 = (xdist[idx[1]]-xdist[idx[0]])/32  #x gap between 1 and 2
            l6 = (ydist[idx[1]]-ydist[idx[0]])/32  #y gap between 1 and 2
            if len(idx) >= 3:
                l7 = (xdist[idx[2]]-xdist[idx[1]])/32  #x gap between 2 and 3
                l8 = (ydist[idx[2]]-ydist[idx[1]])/32  #x gap between 2 and 3
                if len(idx) >=4:
                    l9 = (xdist[idx[3]]-xdist[idx[2]])/32  #etc
                    la = (ydist[idx[3]]-ydist[idx[2]])/32
                    
    return [l1,l2,l5,l6,l7,l8,l9,la,bias]
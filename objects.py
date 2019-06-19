# -*- coding: utf-8 -*-
'''
Contains classes and functions for drawing and manipulating objects
'''
import pygame
import init
from NeuralNet import network
import numpy as np

x_init = init.display_width*0.01
y_init = init.display_height*0.5

player_base = 16
player_height = 16
floor_height = 16
gap_width = 32
switch_width = 32
switch_height = 32
box_idx = []
switch_idx = []
altbox_idx = []

player_floor_1 = y_init - floor_height
player_floor_2 = init.display_height - 2*floor_height

def draw_player(x,y,angle,image):
    #print(f'drawing payer at ({x},{y},{angle})')
    return init.gameDisplay.blit(pygame.transform.rotate(init.Imlist.images[image],angle),(x,y))
    
def draw_floors():
    init.gameDisplay.blit(init.Imlist.images[1],(-gap_width,y_init))
    init.gameDisplay.blit(init.Imlist.images[1],(0,init.display_height - floor_height))
    
def draw_level(lev,rects):
    for obs,x,f in zip(lev.obsarr,lev.obsx,lev.obsfloor):
        for w in range(obs.width):
            for h in range(5):
                if h < obs.height:
                    box_x = int(32*(x + w))
                    box_y = int(f*player_floor_2
                              + (1-f)*player_floor_1
                              - h*32 - floor_height)
                    #print(box_x,box_y)
                    rects.append(init.gameDisplay.blit(init.Imlist.images[2],(box_x,box_y)))
                elif h >= obs.ceil:
                    box_x = int(32*(x + w - (2*f-1)*obs.offset))
                    box_y = int(f*player_floor_2
                              + (1-f)*player_floor_1
                              - h*32 - floor_height)
                    rects.append(init.gameDisplay.blit(init.Imlist.images[2],(box_x,box_y)))

def draw_net(net):
    screencen = init.display_width/2.
    netcen = int(net.layers/2)
    nhist,chist,nnode,nconn = network.get_counts(net)
    max_nodes = max(nhist)

    nodex = np.zeros(nnode,dtype=int)
    nodey = np.zeros(nnode,dtype=int)
    offset = [0,-8,8,-8,0]
    for l in range(net.layers):
        for ii,node in enumerate(net.nodeList[l]):
            nodex[node.nodeNo] = int(screencen + (node.layer - netcen)*64)
            nodey[node.nodeNo] = int(16*(ii+1)*max_nodes/(nhist[l]+1)
            + offset[node.layer])
            
    for l in range(net.layers):
        for ii,conn in enumerate(net.connectionList[l]):
            red = 223 - min(max([0,conn.weight])*96,223)
            blue = 223 - min(abs(conn.weight)*96,223)
            green = 223 - min(-min([0,conn.weight])*96,223)
            pygame.draw.line(init.gameDisplay,(red,green,blue)
                            ,(nodex[conn.fromNode.nodeNo]
                            ,nodey[conn.fromNode.nodeNo])
                            ,(nodex[conn.toNode.nodeNo]
                            ,nodey[conn.toNode.nodeNo])
                            ,2)
                            
    for ii in range(len(nodex)):
        pygame.draw.circle(init.gameDisplay,(0,0,0),(nodex[ii],nodey[ii]),5)
        
def test_collision(x,y,f,lev):
    player_y = y - (1-f)*player_floor_1
    player_y -= f*player_floor_2
    
    for ii,box in enumerate(lev.obsarr):
        if lev.obsfloor[ii] != f:
            continue
        x_lower = lev.obsx[ii]*32 - player_base
        x_upper = (lev.obsx[ii] + box.width)*32
        y_lower = -box.height*32
        y_upper = -box.ceil*32 + player_height
        x_c = x + (2*f-1)*box.offset*32
        
        if x>x_lower and x<x_upper and player_y>y_lower:
            #print(x,y,player_y,x_lower,x_upper,y_lower,y_upper)
            return True
        if x_c>x_lower and x_c<x_upper and player_y<y_upper:
            #print(x,y,player_y,x_lower,x_upper,y_lower,y_upper)
            return True

def look(x,y,f,lev):
    global box_idx
    xdist = np.array(lev.obsx)*32
    boxes = np.array(lev.obsarr)
    width = np.array([obs.width for obs in boxes])
    floor = np.array(lev.obsfloor)
    xdist = xdist - x
    #bottom floor goes backwards
    if f == 1:
        xdist = -xdist
    #get rid of wrong floor and past boxes
    sel = xdist > -(player_base + width*32)
    sel = np.logical_and(sel,floor==f)
    boxes = boxes[sel]
    xdist = xdist[sel]
    
    #order by x distance then y distance ()
    idx = np.argsort(xdist)[:2]
    xdist = xdist[idx]/32
    boxes = boxes[idx]

    bias = 1
    l1,l2,l3,l4,l5,l6 = 0,0,0,0,0,0
    if len(idx) >= 1:
        height = boxes[0].height
        ceil = boxes[0].ceil
        width = boxes[0].width
        offset = boxes[0].offset
        l1 = max(2 - xdist[0]/5,0)  #x dist to next obstacle
        l2 = 2*width/5                #width of next obstacle
        l3 = 2*height/5               #height of next obstacle
        l4 = max(2 - 2*ceil/5,0)      #ceiling of next obstacle
        l5 = 2*offset/5              #relative x position of gap
        if len(idx) >= 2:
            xgap = xdist[1] - (xdist[0] + width)
            l6 = max(2 - xgap/5,0)    #gap between next 2 obs
            #l6 = width[1]              #width of 2nd
            #l7 = height[1]              #height of 2nd
            #l8 = ceil[1]              #ceil of 2nd
    return [l1,l2,l3,l4,l5,l6,bias]


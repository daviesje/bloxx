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
look_verbose = False

player_floor_1 = y_init - player_base
player_floor_2 = init.display_height - floor_height - player_base

pygame.font.init()
myfont = pygame.font.SysFont('Arial',24)

def draw_player(x,y,angle,image):
    return init.gameDisplay.blit(pygame.transform.rotate(init.Imlist.images[image],angle),(x,y))

def draw_scores(ims,scores,lnum):
    surf = myfont.render('level '+str(lnum+1),False,(0,0,0))
    init.gameDisplay.blit(surf,(init.display_width/2,64))
    for ii in range(len(ims)):
        init.gameDisplay.blit(pygame.transform.scale2x(init.Imlist.images[ims[ii]]),(64*(1+ii),32))
        surf = myfont.render(str(scores[ii]),False,(0,0,0))
        init.gameDisplay.blit(surf,(64*(1+ii),96))
    
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
    if f==0:
        player_y = y - player_floor_1
    else:
        player_y = y - player_floor_2
    
    for ii,box in enumerate(lev.obsarr):
        if lev.obsfloor[ii] != f:
            continue
        x_lower = lev.obsx[ii]*32 - player_base
        x_upper = (lev.obsx[ii] + box.width)*32
        y_lower = -box.height*32
        y_upper = -box.ceil*32 + player_base #because -player_floor includes base
        if f == 0:
            x_c = x - box.offset*32
        else:
            x_c = x + box.offset*32
        
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
    
    #bottom floor goes backwards, also add width because of the l-r
    #TODO: place objects in reverse on bottom floor
    if f == 0:
        xdist = xdist - x - player_base
    else:
        xdist = x - xdist - width*32
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
    l1,l2,l3,l4,l5,l6 = -1,-1,-1,1,0,-1
    if len(idx) >= 1:
        height = boxes[0].height
        ceil = boxes[0].ceil
        width = boxes[0].width
        offset = boxes[0].offset
        l1 = 1 - xdist[0]/5     #dist to next box, (10,0) to (-1,1)
        l2 = 2*width/5 - 1      #width of next obstacle, (0,5) to (-1,1)
        l3 = 2*height/5 - 1     #height of next obstacle, (0,5) to (-1,1)
        l4 = 2*ceil/5 - 1       #ceiling of next obstacle, (0,5) to (-1,1)
        l5 = offset/5           #relative x position of gap, (-5,5) to (-1,1)

        if look_verbose:
            print(xdist[0],l1)
        if len(idx) >= 2:
            xgap = xdist[1] - (xdist[0] + width)
            l6 = 1 - xgap/5    #gap between next 2 obs, (10,0) to (-1,1)
            #l6 = width[1]              #width of 2nd
            #l7 = height[1]              #height of 2nd
            #l8 = ceil[1]              #ceil of 2nd
    output = [l1,l2,l3,l4,l5,l6,bias]
    for ii in range(len(output)):
        if output[ii] > 1:
            output[ii] = 1
        elif output[ii] < -1:
            output[ii] = -1
    return output


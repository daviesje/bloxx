# -*- coding: utf-8 -*-
'''
Defines global variables, contains initalisation functions
'''
import pygame

class _imlist():
    def __init__(self):
        self.images = []
        self.names = []
    def add_image(self,fname):
        self.names.append(fname.split('.')[0])
        self.images.append(pygame.image.load(fname))
   
display_width = 1200
display_height = 600
gameDisplay = None
Imlist = _imlist()
    
def load_ims(iml):
    iml.add_image('./Tri_UU_16.png')
    iml.add_image('./Floor.png')
    iml.add_image('./Box.png')
    iml.add_image('./Switch.png')
    iml.add_image('./Tri_Bot_16.png')
    
def init_game():
    pygame.init()

    global Imlist, gameDisplay

    gameDisplay = pygame.display.set_mode((display_width,display_height))

    pygame.display.set_caption('The Ultimate Test Of Skill')
    load_ims(Imlist)
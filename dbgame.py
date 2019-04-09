# -*- coding: utf-8 -*-
import pygame
import objects
import levels
import init
import sys

clock = pygame.time.Clock()

xspeed = 5

init.init_game()
def game_loop():
    ncrashes = 0
    quitting = False

    while not quitting:
        level_win = False
        jumping = False
        fallen = False
        crashed = False
        x = objects.x_init
        y = objects.player_floor_1 
        objects.box_idx = list(range(levels.levelarr[levels.cur_level-1].nbox))
        objects.switch_idx = list(range(levels.levelarr[levels.cur_level-1].nswitch))
        objects.altbox_idx = []

        x_vel = xspeed
        y_vel = 0
        angle = 0
        while not quitting and not crashed and not level_win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitting = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not jumping:
                            jumping = True
                            y_vel = -12
                                
            x = x + x_vel
            y = y + y_vel
                                
            if jumping:
                y_vel = y_vel + 0.5
                if fallen:
                    angle = angle + 5
                else:
                    angle = angle - 5
                                    
            if not fallen:
                if y > objects.player_floor_1:
                    y = objects.player_floor_1
                    y_vel = 0
                    jumping = False
                    angle = 0
            elif y > objects.player_floor_2:
                y = objects.player_floor_2
                x_vel = -xspeed
                y_vel = 0
                jumping = False
                angle = 0

            crashed = objects.test_collision(x,y,levels.cur_level)

            if x > init.display_width - objects.player_base:
                x = init.display_width - objects.player_base
                x_vel = 0
                fallen = True
                jumping = True
        
            if fallen and x < 0:
                x = objects.x_init
                y = objects.player_floor_1
                level_win = True
                levels.next_level()

            init.gameDisplay.fill((255,255,255))
            objects.draw_player(x,y,angle)
            objects.draw_level(levels.cur_level)
            objects.draw_floors()
            
            pygame.display.update()
            clock.tick(60)
            
        if crashed:
            ncrashes = ncrashes + 1
        if level_win:
            pygame.time.wait(500)
        
game_loop()    
pygame.quit()
sys.exit()
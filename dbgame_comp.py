# -*- coding: utf-8 -*-
import pygame
from NeuralNet import network
import objects
import levels
import init
import sys
import player
import numpy as np

clock = pygame.time.Clock()

jump_v = -12
place_human = True
continue_game = True

init.init_game()
def game_loop():
    #game layer
    opponent_1 = 'saves/best_bot_std'
    opponent_2 = 'saves/best_bot_hard'
    opponent_3 = 'saves/best_bot_wow'
    opponents = [opponent_1,opponent_2,opponent_3]
    nplayers = len(opponents)
    quitting = False
    draw_game = True
    speed = 1

    #generate first gen of players
    bot_list = []
    human = []
    
    for ii,bot in enumerate(opponents):
        bot_list.append(player.Player())
        bot_list[ii].net = network.load_net(bot)
        bot_list[ii].image = 4 + ii
        
    if place_human:
        human = [player.Human()]

    while not quitting:
        ###GENERATION LAYER###
        if len(levels.levelarr) > 0:
            levels.cur_level = levels.levelarr[0]
        else:
            levels.cur_level = levels.generate_level(0)
            
        levels.cur_level_n = 0

        ndead = 0
        while levels.cur_level_n < 10 and not quitting:
            ###LEVEL LAYER###            
            #reset level
            nwin = 0
            ndead = 0
            give_up = False
            for bn,tri in enumerate(bot_list + human):
                #comp mode, reset all players
                tri.x_pos = objects.x_init
                tri.x_pos -= (len(bot_list) - bn)*64
                tri.y_pos = objects.player_floor_1 
                tri.jumping = False
                tri.fallen = False
                tri.x_vel = player.xspeed
                tri.y_vel = 0
                tri.angle = 0
                tri.win = False
                tri.dead = False
                    
            levelrects = []
            #display bg, floors and net
            init.gameDisplay.fill((255,255,255))
            if draw_game:
                objects.draw_level(levels.cur_level,levelrects)
                objects.draw_floors()
            pygame.display.update()
            
            if place_human:
                pygame.time.wait(1000)

            activerects = []
            while ndead + nwin < nplayers + place_human:
                ###TICK LAYER###
                prevrects = activerects
                activerects = [] #active parts to update on screen
                #fill in previous positions
                if draw_game:
                    init.gameDisplay.fill((255,255,255))
                    #for rect in prevrects:
                        #init.gameDisplay.fill((255,255,255),rect=rect)
                        
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quitting = True
                        ndead = len(bot_list) + 5
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and place_human:
                            if not human[0].jumping:
                                human[0].jumping = True
                                human[0].y_vel = jump_v

                        if event.key == pygame.K_PERIOD:
                            speed = 128
                        if event.key == pygame.K_COMMA:
                            speed = 1
                        if event.key == pygame.K_g:
                            draw_game = not draw_game
                        if event.key == pygame.K_r:
                            give_up = True
                        if event.key == pygame.K_p:
                            print(inputs)
                            print(decision)
                            print(ndead,nwin)
                                
                for bot in bot_list:
                    #only decide if not in air
                    if not bot.jumping and not bot.dead:
                        inputs = objects.look(bot.x_pos,bot.y_pos,bot.fallen
                                              ,levels.cur_level)
                        decision = bot.net.propogate(inputs)
                        if decision > 0:
                            bot.jumping = True
                            bot.y_vel = jump_v

                for tri in bot_list + human:
                    ###PLAYER LOOP###
                    if tri.dead or tri.win:
                        continue
                    
                    if tri.jumping:
                        tri.y_vel = tri.y_vel + 0.5
                        if tri.fallen:
                            #tri.angle = 0
                            tri.angle = tri.angle + 5
                        else:
                            #tri.angle = 0
                            tri.angle = tri.angle - 5

                    #UPDATE POSITION
                    tri.x_pos = tri.x_pos + tri.x_vel
                    tri.y_pos = tri.y_pos + tri.y_vel
                    #FLOOR COLLISIONS                
                    if not tri.fallen:
                        if tri.y_pos > objects.player_floor_1:
                            tri.y_pos = objects.player_floor_1
                            tri.y_vel = 0
                            tri.jumping = False
                            tri.angle = 0
                    elif tri.y_pos > objects.player_floor_2:
                        tri.y_pos = objects.player_floor_2
                        tri.x_vel = -player.xspeed
                        tri.y_vel = 0
                        tri.jumping = False
                        tri.angle = 0

                    if tri.x_pos > init.display_width - objects.player_base:
                        tri.x_pos = init.display_width - objects.player_base
                        tri.y_pos = objects.player_floor_1
                        tri.y_vel = 0
                        tri.x_vel = 0
                        tri.fallen = True
                        tri.jumping = True
                    
                    if tri.fallen and tri.x_pos < 0:
                        tri.win = True
                        nwin += 1
                    #CHECK FOR CRASH
                    crashed = objects.test_collision(tri.x_pos,tri.y_pos,tri.fallen,levels.cur_level)
                    if crashed:
                        tri.dead = True
                        tri.crashes += 1
                        ndead += 1
                    #DRAW IF NOT CRASHED
                    elif draw_game:
                        activerects.append(objects.draw_player(tri.x_pos,tri.y_pos,tri.angle,tri.image))
                    
                    tri.score += 1

                #END OF TICK LAYER
                if draw_game:
                    objects.draw_level(levels.cur_level,levelrects)
                    objects.draw_floors()
                    scores = [bot_list[0].crashes,bot_list[1].crashes
                              ,bot_list[2].crashes,human[0].crashes]
                    scims = [bot_list[0].image,bot_list[1].image
                              ,bot_list[2].image,human[0].image]
                    
                    objects.draw_scores(scims,scores,levels.cur_level_n)
                    #updaterects = prevrects + activerects
                    pygame.display.update()

                clock.tick(60*speed)
                
            #END OF LEVEL LAYER
            if levels.cur_level_n < levels.num_levels or continue_game:
                levels.next_level()
            else:
                quitting = True
                ndead = nplayers + 5

        #END OF GEN LAYER wait to display scores
        pygame.time.wait(15000)
        quitting = True

game_loop()    
pygame.quit()
sys.exit()
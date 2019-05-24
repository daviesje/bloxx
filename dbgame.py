# -*- coding: utf-8 -*-
import pygame
from NeuralNet import network
import objects
import levels
import init
import sys
import player
import numpy as np
from copy import deepcopy

clock = pygame.time.Clock()

jump_v = -12
nplayers = 100
place_human = False

init.init_game()
def game_loop():
    #game layer
    best_bot = None
    #startnet = 'saves/best_bot_0'
    startnet = None
    quitting = False
    draw_game = True
    speed = 1

    #generate first gen of players
    bot_list = []
    human = []
    for ii in range(nplayers):
        bot_list.append(player.Player())
    
    if startnet is not None:
        bot_list[len(bot_list) - 1].net = network.load_net(startnet)

    if place_human:
        human = [player.Human()]

    best_bot = bot_list[len(bot_list) - 1]
    #TODO: ADD GENERATION LAYER
    while not quitting:
        #generation layer
        levels.cur_level = 1
        objects.box_idx = list(range(levels.levelarr[levels.cur_level-1].nbox))

        maxscore = 0
        ndead = 0
        while ndead < len(bot_list + human):
            #level layer            
            #reset level
            nwin = 0
            give_up = False
            for tri in bot_list + human:
                if not tri.dead:
                    tri.x_pos = objects.x_init
                    tri.y_pos = objects.player_floor_1 
                    tri.jumping = False
                    tri.fallen = False
                    tri.x_vel = player.xspeed
                    tri.y_vel = 0
                    tri.angle = 0
                    tri.win = False
            if draw_game:
                init.gameDisplay.fill((255,255,255))
                objects.draw_level(levels.cur_level)
                objects.draw_floors()
            objects.draw_net(best_bot.net)

            pygame.display.update()
            if place_human:
                pygame.time.wait(750)
            while ndead + nwin < nplayers + place_human:
                #tick layer
                init.gameDisplay.fill((255,255,255))
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
                            speed = speed*2
                            if speed > 128:
                                speed = 128
                            print(speed)

                        if event.key == pygame.K_COMMA:
                            speed = speed/2
                            if speed < 1/32.:
                                speed = 1/32.
                            print(speed)
                        if event.key == pygame.K_g:
                            draw_game = not draw_game
                        if event.key == pygame.K_r:
                            give_up = True
                            
                for bot in bot_list:
                    #only decide if not in air
                    if not bot.jumping and not bot.dead:
                        inputs = objects.look(bot.x_pos,bot.y_pos,bot.fallen,levels.cur_level)
                        decision = bot.net.propogate(inputs)
                        if decision > 0:
                            bot.jumping = True
                            bot.y_vel = jump_v

                for tri in bot_list + human:
                    if tri.dead or tri.win:
                        continue

                    if draw_game:
                        objects.draw_player(tri.x_pos,tri.y_pos,tri.angle,tri.image)

                    crashed = objects.test_collision(tri.x_pos,tri.y_pos,levels.cur_level)
                    if crashed:
                        tri.dead = True
                        ndead += 1
                    
                    if tri.jumping:
                        tri.y_vel = tri.y_vel + 0.5
                        if tri.fallen:
                            tri.angle = tri.angle + 5
                        else:
                            tri.angle = tri.angle - 5
                                    
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

                    #END OF PLAYER LOOP
                    tri.x_pos = tri.x_pos + tri.x_vel
                    tri.y_pos = tri.y_pos + tri.y_vel
                    tri.score += 1

                #END OF TICK LAYER
                if place_human and human[0].dead and not give_up:
                    human[0].dead = False
                    ndead -= 1
                    human[0].x_pos = objects.x_init
                    human[0].y_pos = objects.player_floor_1 
                    human[0].jumping = False
                    human[0].fallen = False
                    human[0].x_vel = player.xspeed
                    human[0].y_vel = 0
                    human[0].angle = 0
                    human[0].win = False

                if draw_game:
                    objects.draw_level(levels.cur_level)
                    objects.draw_floors()

                objects.draw_net(best_bot.net)
                pygame.display.update()
                clock.tick(60*speed)
                
            #END OF LEVEL LAYER
            if(nwin > 0):
                rlevel = levels.next_level()
                if rlevel:
                    lev = levels.generate_level(levels.cur_level)
                    levels.levelarr.append(lev)
                objects.box_idx = list(range(levels.levelarr[levels.cur_level-1].nbox))
                #starting new level
                #objects.switch_idx = list(range(levels.levelarr[levels.cur_level-1].nswitch))
                #objects.altbox_idx = []


        #END OF GEN LAYER, dont mutate if quitting
        if not quitting:
            scores = np.zeros(nplayers)
            for ii,tri in enumerate(bot_list):
                scores[ii] = int(tri.score) + np.random.rand()
                tri.dead = False
                tri.score = 0
                
            #reset human
            if place_human:
                human[0].dead = False
                human[0].score = 0

            if scores.max() > maxscore:
                maxscore = scores.max
    
            idx = np.argsort(scores)
            buf = []
            for ii in idx[int(nplayers/2):]:
                buf.append(bot_list[ii])
                
            bot_list = buf
            best_bot = bot_list[len(bot_list)-1]
            #print best net
            for conn in best_bot.net.connectionList:
                print(f'wgt {conn.weight:6.3f} | from {conn.fromNode.nodeNo:3d}'
                        +f'to {conn.toNode.nodeNo:3d} | lyr {conn.layer:3d}')
    
            print(f'----------{scores[idx[-1]]:.2f}------------')
            for ii in range(int(nplayers/2)):
                newbot = deepcopy(bot_list[ii])
                newbot.net.mutate()
                bot_list.append(newbot)
            
    svweights = []
    svfnodes = []
    svtnodes = []
    svnoden = []
    svnodel = []
    for conn in best_bot.net.connectionList:
        svweights.append(conn.weight)
        svfnodes.append(conn.fromNode.nodeNo)
        svtnodes.append(conn.toNode.nodeNo)
    
    for node in best_bot.net.nodeList:
        svnodel.append(node.layer)
        svnoden.append(node.nodeNo)
    
    svconn = np.array([svweights,svfnodes,svtnodes])
    svconn = svconn.T
    svnodes = np.array([svnoden,svnodel])
    svnodes = svnodes.T
    if startnet is not None:
        np.savetxt(startnet+'_c.txt',svconn,delimiter='\t')
        np.savetxt(startnet+'_n.txt',svnodes,delimiter='\t')
    else:
        np.savetxt('./saves/best_bot_new_c.txt',svconn,delimiter='\t')
        np.savetxt('./saves/best_bot_new_n.txt',svnodes,delimiter='\t')

game_loop()    
pygame.quit()
sys.exit()
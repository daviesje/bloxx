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
nplayers = 20
place_human = False
continue_game = True
full_nets = False

init.init_game()
def game_loop():
    #game layer
    best_bot = None
    #startnet = 'saves/best_bot_full'
    startnet = None
    quitting = False
    draw_game = True
    speed = 1

    #generate first gen of players
    bot_list = []
    human = []
    for ii in range(nplayers):
        pbuf = player.Player()
        if full_nets:
            pbuf.net = network.full_network()
            pbuf.net.mutate()
        bot_list.append(pbuf)
    
    if startnet is not None:
        bot_list[len(bot_list) - 1].net = network.load_net(startnet)

    if place_human:
        human = [player.Human()]

    best_bot = bot_list[len(bot_list) - 1]
    while not quitting:
        ###GENERATION LAYER###
        if len(levels.levelarr) > 0:
            levels.cur_level = levels.levelarr[0]
        else:
            levels.cur_level = levels.generate_level(0)
            
        levels.cur_level_n = 0

        ndead = 0
        while ndead < len(bot_list + human):
            ###LEVEL LAYER###            
            #reset level
            nwin = 0
            give_up = False
            for bn,tri in enumerate(bot_list + human):
                if not tri.dead:
                    tri.x_pos = objects.x_init
                    tri.y_pos = objects.player_floor_1 
                    tri.jumping = False
                    tri.fallen = False
                    tri.x_vel = player.xspeed
                    tri.y_vel = 0
                    tri.angle = 0
                    tri.win = False
                    
            levelrects = []
            inputs = [0,0,0,0,0,0,0]
            decision = 0
            #display bg, floors and net
            init.gameDisplay.fill((255,255,255))
            objects.draw_net(best_bot.net)
            if draw_game:
                objects.draw_level(levels.cur_level,levelrects)
                objects.draw_floors()
            pygame.display.update()
            
            if place_human:
                pygame.time.wait(750)

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
                            speed = 256
                        if event.key == pygame.K_COMMA:
                            speed = 1
                        if event.key == pygame.K_g:
                            draw_game = not draw_game
                        if event.key == pygame.K_r:
                            give_up = True
                        if event.key == pygame.K_p:
                            print(inputs)
                            print(decision)
                            #objects.look_verbose = not objects.look_verbose
                            #speed = 1/8
                                
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
                        ndead += 1
                        #print(inputs)
                    #DRAW IF NOT CRASHED
                    elif draw_game:
                        activerects.append(objects.draw_player(tri.x_pos,tri.y_pos,tri.angle,tri.image))
                    
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
                    objects.draw_level(levels.cur_level,levelrects)
                    objects.draw_floors()
                    objects.draw_net(best_bot.net)
                    #updaterects = prevrects + activerects
                    pygame.display.update()

                clock.tick(60*speed)
                
            #END OF LEVEL LAYER
            if(nwin > 0):
                if levels.cur_level_n < levels.num_levels or continue_game:
                    levels.next_level()
                else:
                    quitting = True
                    ndead = nplayers + 5

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
    
            cull_length = int(len(bot_list)/2)
            idx = np.argsort(scores)
            buf = []
            for ii in idx[cull_length:]:
                buf.append(bot_list[ii])
                
            bot_list = buf
            best_bot = bot_list[len(bot_list)-1]

            print(f'----------{scores[idx[-1]]:7.2f}'
                               +f'------------{levels.cur_level_n}')
            for ii in range(cull_length):
                idx = ii%cull_length
                newbot = deepcopy(bot_list[::-1][idx])
                newbot.net.mutate()
                bot_list.append(newbot)
            
    svweights = []
    svfnodes = []
    svtnodes = []
    svnoden = []
    svnodel = []
    for l in range(best_bot.net.layers):
        for conn in best_bot.net.connectionList[l]:
            svweights.append(conn.weight)
            svfnodes.append(conn.fromNode.nodeNo)
            svtnodes.append(conn.toNode.nodeNo)
    
        for node in best_bot.net.nodeList[l]:
            svnodel.append(node.layer)
            svnoden.append(node.nodeNo)
    
    svconn = np.array([svweights,svfnodes,svtnodes])
    svconn = svconn.T
    svnodes = np.array([svnoden,svnodel])
    svnodes = svnodes.T
    if startnet is not None and False:
        np.savetxt(startnet+'_c.txt',svconn,delimiter='\t')
        np.savetxt(startnet+'_n.txt',svnodes,delimiter='\t')
    else:
        np.savetxt('./saves/best_bot_new_c.txt',svconn,delimiter='\t')
        np.savetxt('./saves/best_bot_new_n.txt',svnodes,delimiter='\t')

game_loop()    
pygame.quit()
sys.exit()
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:53:50 2019

@author: jed12
"""
from math import exp
import numpy as np
from numpy.random import rand, randint, randn

def load_net(fname):
    conn_arr = np.loadtxt(fname+'_c.txt',delimiter='\t')
    node_arr = np.loadtxt(fname+'_n.txt',delimiter='\t').astype(int)
    net = Network()
    net.nodeList = []
    net.connectionList = []
    for row in node_arr:
        net.add_node(row[1])
    for row in conn_arr:
        net.add_connection(net.nodeList[int(row[1])],net.nodeList[int(row[2])],row[0])
    net.layers = (node_arr[:,1]).max() + 1    
    return net

class Connection():
    def __init__(self):
        self.connectionno = -1
        self.fromNode = None
        self.toNode = None
        self.weight = 0
        self.layer = 1 #To layer
    def engage(self):
        self.toNode.input += self.fromNode.output*self.weight

class Node():
    def __init__(self,layer=0):
        self.nodeNo = -1
        self.layer = -1
        self.input = 0
        self.output = 0
    #sigmoid input -> output
    def engage(self):
        self.output = 2 / (1 + exp(-self.input)) - 1
        
class Network():
    def __init__(self):
        self.nodeList = []
        self.connectionList = []
        self.layers = 2
        self.add_node(layer=0) #x distance to next object
        self.add_node(layer=0) #y distance to next object
        #self.add_node(layer=0) #x width of next object
        #self.add_node(layer=0) #y width of next object
        self.add_node(layer=0) #x gap between next 2 objects
        self.add_node(layer=0) #y gap between next 2 objects
        self.add_node(layer=0) #x gap between next 3 objects
        self.add_node(layer=0) #y gap between next 3 objects
        self.add_node(layer=0) #x gap between next 4 objects
        self.add_node(layer=0) #y gap between next 4 objects
        self.looknodes = self.add_node(layer=0).nodeNo #bias
        self.add_node(layer=1) #output node
        self.add_connection(self.nodeList[self.looknodes],self.nodeList[self.looknodes+1],1)
        #self.add_connection(self.nodeList[0],self.nodeList[self.looknodes+1],-1)
    def add_node(self,layer):
        n = len(self.nodeList) 
        newnode = Node()
        newnode.nodeNo = n
        newnode.layer = layer
        self.nodeList.append(newnode)
        return newnode
    def add_connection(self,fromnode,tonode,weight):
        assert fromnode.layer < tonode.layer
        n = len(self.connectionList)
        newcon = Connection()
        newcon.fromNode = fromnode
        newcon.toNode = tonode
        newcon.layer = tonode.layer
        newcon.weight = weight
        newcon.connectionno = n
        self.connectionList.append(newcon)
        return newcon
    def propogate(self,sights):
        self.reset_network()
        for i,lnode in enumerate(self.nodeList[:self.looknodes+1]):
            #print(i,sights)
            lnode.output = sights[i]
        for layer in range(1,self.layers):
            for c in self.connectionList:
                if c.layer == layer:
                    c.engage()
                    #print(f'connection {c.connectionno} engaged')
            for n in self.nodeList:
                if n.layer == layer:
                    n.engage()
                    #print(f'node {c.connectionno} engaged, in: {n.input} out: {n.output}')
        return self.nodeList[self.looknodes+1].output
    def reset_network(self):
        for n in self.nodeList:
            n.input = 0
            n.output = 0
    def mutate(self,manual=0):
        switch = rand()
        if manual==1:
            switch = 0.5
        elif manual==2:
            switch = 0.95
        elif manual==3:
            switch = 0.999
        #90% change weight on random connection
        if switch < 0.90:
            for conn in self.connectionList:
                rand2 = rand()
                if rand2 < 0.1:
                    conn.weight = (2*rand()-1)
                else:
                    conn.weight += (randn()*0.1)
        #9% add connection between random nodes
        elif switch < 0.98:
            wgt = 2*rand()-1
            badnodes = True
            #check if fully connected
            if self.fully_connected():
                print('already fully connected')
                return -1
            #check if nodes eligible, continue until found
            while badnodes:
                badnodes = False
                sel1 = randint(len(self.nodeList))
                sel2 = randint(len(self.nodeList))
                n1 = self.nodeList[sel1]
                n2 = self.nodeList[sel2]
                lr = n1.layer < n2.layer
                if n1.layer == n2.layer:
                    badnodes = True
                    continue
                for c in self.connectionList:
                    if c.fromNode == n1 and c.toNode == n2:
                        badnodes = True
                        break
                    elif c.fromNode == n2 and c.toNode == n1:
                        badnodes = True
                        break
            #print(f'adding connection between nodes {sel1}, {n1.layer} and {sel2}, {n2.layer}: weight = {wgt} ')
            if(lr):
                self.add_connection(n1,n2,wgt)
            else:
                self.add_connection(n2,n1,wgt)
        #1% add new node by splittting random connection
        else:
            if len(self.connectionList) == 1:
                #can't I?
                print('cant split bias-output connection')
                return
            tolayer = 1
            fromlayer = 0

            #TODO: FIND A DO/WHILE LOOP
            sel = randint(1,len(self.connectionList))
            conn = self.connectionList[sel]
            tolayer = conn.layer
            fromlayer = conn.fromNode.layer

            while tolayer == fromlayer + 1 and self.layers == 6:
                sel = randint(1,len(self.connectionList))
                conn = self.connectionList[sel]
                tolayer = conn.layer
                fromlayer = conn.fromNode.layer

            tonode = conn.toNode
            fromnode = conn.fromNode
            wgt = conn.weight
            #REMOVE CONNECTION
            self.connectionList.remove(conn)
            #ADD LAYER IF NEEDED
            if tolayer == fromlayer + 1:
                self.layers +=1
                for c in self.connectionList:
                    if c.layer >= tolayer:
                        c.layer +=1
                for n in self.nodeList:
                    if n.layer >= tolayer:
                        n.layer +=1
                newlayer = tolayer
            else:
                newlayer = randint(fromlayer+1,tolayer)
            #ADD NODE
            #print(f'adding node in connection {sel}, layers {fromlayer,newlayer,tolayer}')
            newnode = self.add_node(newlayer)
            #ADD CONNECTIONS
            self.add_connection(fromnode,newnode,wgt)
            self.add_connection(newnode,tonode,wgt)
    def fully_connected(self):
        nhist = [0]*self.layers
        maxcon = 0
        for n in self.nodeList:
            nhist[n.layer] += 1
        for n in self.nodeList:
            l = int(n.layer + 1)
            for x in nhist[l:]:
                maxcon = maxcon + x
        return len(self.connectionList) >= maxcon
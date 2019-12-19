#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:10:19 2019

@author: JakeCillay
"""

class Combo:
    def __init__(self,problem):
        pass

    def eval(self, state):
        linger = 0
        index = 0
        for x in state[2]:
            
            
            if x != 'X' and x != ' ' :
                letter = x
                if state[1][index] == linger:
                    if state[0][index] != ' ' and state[0][index] != x:
                        linger += 1
                elif state[3][index] == letter:
                    if state[4][index] != ' ' and state[4][index] != x:
                        linger += 1
                    else:
                        if state[5][index] != letter and state[5][index] != ' ':
                            linger += 1
                else:
                    if state[1][index] != ' ' or state[3][index] != ' ':
                        linger += 1
            if(index == 6):
                break
            index += 1
        num_carscount = 0
        for x in state[2]:
            if x != 'X' and x != ' ' :
                num_carscount+= 1
    
        return num_carscount + linger
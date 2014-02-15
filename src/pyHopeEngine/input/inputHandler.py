'''
Created on May 7, 2013

@author: Devon

Defines input handlers
'''

import pygame

class KeyboardHandler(object):
    '''Base handler for keyboard input'''
    def __init__(self):
        '''Create a new keyboard handler'''
        #list of all keyboard keys
        self.keys = list(pygame.key.get_pressed())
    
    
    def onKeyDown(self, key):
        self.keys[key] = True
    
    
    def onKeyUp(self, key):
        self.keys[key] = False
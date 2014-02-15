'''
Created on Aug 2, 2013

@author: Devon

Defines main audio system
'''

import pygame

from pyHopeEngine import engineCommon as ECOM

class Audio:
    '''Main audio system.'''
    
    def __init__(self):
        self.soundDict = {}
    
    def addSound(self, file, name):
        '''Add a sound to the dictionary
        
        Keyword arguments:
            file -- file path of the sound
            name -- name to be associated with sound
        '''
        
        file = ECOM.engine.resourceManager.getFile(file)
        sound = pygame.mixer.Sound(file)
        self.soundDict[name] = sound
    
    def playSound(self, name):
        self.soundDict[name].play()
    
    def setBackgroundMusic(self, file):
        pygame.mixer.music.load(file)
    
    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1, 0.0)
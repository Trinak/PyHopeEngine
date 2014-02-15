'''
Created on May 29, 2013

@author: Devon

Defines a game sprite
'''

import pygame

from pyHopeEngine import engineCommon as ECOM

class GameSprite(pygame.sprite.Sprite):
    '''Base game sprite image'''
    
    def __init__(self, file):
        pygame.sprite.Sprite.__init__(self)
        
        file = ECOM.engine.resourceManager.getFile(file)
        self.image = pygame.image.load(file)
        self.oriImage = pygame.image.load(file)


class SpriteSheet(object):
    '''A SpriteSheet object'''
    def __init__(self, image, rect, numImages):
        self.image = image
        self.rect = rect
        self.numImages = numImages
        self.imageList = []
        
        self.createImageList()
    
    def createImageList(self):
        self.imageList =[self.splitSpriteSheet(self.rect, i) for i in range(0, self.numImages)]
        
        return
        
    def splitSpriteSheet(self, rect, index):
        tempRect = pygame.Rect(rect)
        tempRect.left *= index
        surface = pygame.Surface(rect.size)
        surface.blit(self.image, (0, 0), tempRect)
        
        return surface
    
    def returnImageList(self):
        return self.imageList
    
    def returnImageAtIndex(self, index):
        return self.imageList[index]
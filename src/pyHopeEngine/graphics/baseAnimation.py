'''
Created on Oct 22, 2013

@author: Devon Arrington
'''

import pyganim


class BaseAnimation(object):
    '''Base animation. Should be subclassed to add details'''
    def __init__(self):
        self.animation = None
        self.rect = None
    
    def loadAnimation(self, frames, loop = True):
        self.animation = pyganim.PygAnimation(frames, loop)
    
    def setup(self, pos, angle):
        rect = self.rect
        rect.x = pos.x
        rect.y = pos.y
        animation = self.animation.getCopy()
        animation.rotate(angle)
        rect = animation._transformedImages[0].get_rect(center = rect.center)
        return (animation, rect)
    
    def getTransformedRect(self, index, **kwargs):
        '''Returns a rect using pygames Surface get_rect method'''
        return self.animation._transformedImages[index].get_rect(**kwargs)
    
    def getMaxTransformSize(self):
        '''Returns the max width and height of the transformed Surfaces'''
        frameWidths = []
        frameHeights = []
        for i in range(len(self.animation._transformedImages)):
            frameWidth, frameHeight = self.animation._transformedImages[i].get_size()
            frameWidths.append(frameWidth)
            frameHeights.append(frameHeight)
        maxWidth = max(frameWidths)
        maxHeight = max(frameHeights)

        return (maxWidth, maxHeight)
    
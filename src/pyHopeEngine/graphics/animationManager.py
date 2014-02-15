'''
Created on Oct 14, 2013

@author: Devon Arrington
'''

import pyganim

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Event_PlayAnimation

class AnimationManager(object):
    '''Manages animations'''
    def __init__(self, renderer):
        self.animations = {}
        self.animToDraw = []
        self.displaySurface = renderer.displaySurface
        ECOM.eventManager.addListener(self.playEvent, Event_PlayAnimation.eventType)
    
    def loadAnimation(self, name, animation):
        '''Load animations to dictionary.
        
        Keyword arguments:
            name - reference to animation
            animation - the animation to add to the manager
        '''
        
        if name not in self.animations:
            self.animations[name] = animation
    
    def playAnimation(self, name, pos, angle):
        '''Adds an animation to the queue and sets its state to PLAYING'''
        anim = self.animations[name]
        animation, rect = anim.setup(pos, angle)
        animation.play()
        self.animToDraw.append((animation, rect))
        
    def stopAnimation(self, name):
        self.animations[name].stop()
    
    def pauseAnimation(self, name):
        self.animations[name].pause()
    
    def getAnimation(self, name):
        return self.animations[name]
        
    def render(self):
        '''Draws the animations in the queue.'''
        for i in range(len(self.animToDraw) - 1, -1, -1):
            self.animToDraw[i][0].blit(self.displaySurface, self.animToDraw[i][1])
            
            if self.animToDraw[i][0].state == pyganim.STOPPED:
                del self.animToDraw[i]

    def playEvent(self, event):
        self.playAnimation(event.name)
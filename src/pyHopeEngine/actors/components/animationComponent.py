'''
Created on Nov 6, 2013

@author: Devon Arrington
'''

import pygame

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.actors.components.renderComponent import RenderComponent
from pyHopeEngine.graphics.sceneNode import AnimationNode

class AnimationComponent(RenderComponent):
    def __init__(self):
        super().__init__()
        self.frames = []
        
    def init(self, element):
        ''' Initializes the component from an XML file
        
        Keyword arguments:
            element - the XML node containing this component
        '''
        frameElement = element.find("Frames")
        for child in frameElement:
            frame = child[0].text
            frame = ECOM.engine.resourceManager.getFile(frame)
            time = eval(child[1].text)
            self.frames.append((frame, time))
                
        
        loopElement = element.find("Loop")
        self.loop = eval(loopElement.text)
    
    def createSceneNode(self):
        '''Creates a corresponding scene node'''
        transformComponent = self.owner.getComponent("TransformComponent")
        
        if transformComponent.pos is not None:
            pos = transformComponent.pos
            size = transformComponent.size
        else:
            pos = (0, 0)
            size = (100, 100)
        
        rect = pygame.Rect(pos, size)
        sceneNode = AnimationNode(self.owner.actorID, self, self.frames, self.loop, rect)
        
        return sceneNode
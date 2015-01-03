'''
Created on May 31, 2013

@author: Devon

Defines the human view
'''

import pygame
import pygame.locals as pyLocals

from pyHopeEngine import GameView, Audio, Scene
from pyHopeEngine import engineCommon as ECOM

class HumanView(GameView):
    '''Main view for players'''
    def __init__(self, renderer = None):
        self.audio = Audio()
        self.keyboardHandler = None
        self.mouseHandler = None
        self.background = None
        self.screenElement = []
        
        if renderer is not None:
            self.scene = Scene(renderer)     
        
        self.viewID = None
        self.actorID = None
        self.controlledActor = None
        self.type = "HumanView"
    
    def cleanUp(self):
        for screen in self.screenElement:
            screen.cleanUp()
            
    def setControlledActor(self, actorID):
        self.actorID = actorID
        self.controlledActor = self.scene.findNode(self.actorID)

    def setBackground(self, file):
        file = ECOM.engine.resourceManager.getFile(file)
        self.background = pygame.image.load(file).convert()

    def addScreenElement(self, element):
        '''Add UI or Scene elements to the view'''
        self.screenElement.append(element)
    
    def onPygameEvent(self, event):
        if event.type == pyLocals.KEYDOWN:
            self.keyboardHandler.onKeyDown(event.key)
        if event.type == pyLocals.KEYUP:
            self.keyboardHandler.onKeyUp(event.key)
    
    def render(self):
        if self.background is not None:
            self.scene.renderer.render(self.background, [0, 0])
        
        for element in self.screenElement:
            element.render()
    
    def update(self):
        pass
        
        
            
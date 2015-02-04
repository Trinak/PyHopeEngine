'''
Created on Jun 3, 2013

@author: Devon

Defines main engine

Note: Engine heavily inspired by the Game Coding Complete
Engine created by Mike McShaffry and David "Rez" Graham
and used in their book by the same name.
'''

import sys
import pygame
import pygame.locals as pyLocals

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import ClientManager, ServerManager, NetworkEventForwarder
from pyHopeEngine import Renderer
from pyHopeEngine import EventManager
from pyHopeEngine import ResourceManager

pygame.init()

class PyHopeEngineApp:
    '''The main engine.'''
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.renderer = Renderer()
        self.resourceManager = ResourceManager()
        self.eventManager = EventManager()
        self.fps = 60
        self.baseLogic = None
        self.networkManager = None
        self.caption = ''
        self.renderFlags = 0
        self.runGame = True
        
        #Set the global engine and event manager
        ECOM.engine = self
        ECOM.eventManager = self.eventManager

    def run(self):
        '''Main loop of the engine'''
        self.initGame()
        
        while self.runGame:
            elapsedTime = self.clock.get_time()
            self.handlePygameEvents()
            self.eventManager.update()
            
            if self.networkManager is not None:
                self.networkManager.update()
            
            self.baseLogic.update(elapsedTime)
            
            self.renderer.clearSurface(ECOM.Colors.BLACK)
            for view in self.baseLogic.gameViewList:
                view.render()
            
            if ECOM.Debug.PHYSICS:
                self.baseLogic.physics.debugDraw()
            
            pygame.display.update()
            self.clock.tick(self.fps)
    
    def initGame(self):
        '''Initialize the renderer and game'''
        self.renderer.initMainSurface(self.caption, self.renderFlags)
        self.createLogicAndView()
        ECOM.actorManager = self.baseLogic.actorManager
                   
    def createLogicAndView(self):
        raise NotImplementedError("createLogicAndView not implemented.")
        
    def handlePygameEvents(self):
        '''Handles events created through pygame'''
        inputEvents = [pyLocals.KEYDOWN, pyLocals.KEYUP, pyLocals.MOUSEMOTION, 
                       pyLocals.MOUSEBUTTONUP, pyLocals.MOUSEBUTTONDOWN]
        for event in pygame.event.get():
            if event.type == pyLocals.QUIT:
                self.terminate()
            elif event.type in inputEvents:
                if event.type == pyLocals.KEYDOWN:
                    if event.key == pyLocals.K_ESCAPE:
                        self.terminate()
                for view in self.baseLogic.gameViewList:
                    view.onPygameEvent(event)

    def setupClient(self):
        '''Sets up a client network manager'''
        self.networkManager = ClientManager()
        self.networkManager.init()
    
    def setupServer(self):
        '''Sets up a server network manager'''
        self.networkManager = ServerManager()
        self.networkManager.init()
        
    def createNetworkEventForwarder(self):
        '''Creates an event forwarder for clients and server to communicate'''
        self.networkEventForwarder = NetworkEventForwarder()

    def cleanUp(self):
        if self.networkManager is not None:
            self.networkManager.cleanUp()
        
        if self.baseLogic is not None:
            self.baseLogic.cleanUp()
    
    def terminate(self):
        self.cleanUp()
        pygame.quit()
        sys.exit()
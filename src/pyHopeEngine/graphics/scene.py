'''
Created on Jun 7, 2013

@author: Devon

Defines a scene graph holding the world objects
'''

from pygame import Rect
from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Event_NewRenderComponent, Event_ActorMoved, Event_DestroyActor, Event_ScreenResize, Event_PlayAnimation
from pyHopeEngine.sceneNode import RootNode, CameraNode

class Scene:
    '''Main scene graph'''
    
    def __init__(self, renderer):
        '''Creates a new scene graph
        
        Keyword arguments:
            renderer -- the main renderer
        '''
        
        self.rootNode = RootNode()
        self.renderer = renderer
        width = renderer.displaySurface.get_width()
        height = renderer.displaySurface.get_height()
        self.camera = CameraNode(width, height)
        self.viewRect = Rect(0, 0, 0, 0)
        
        #Dictionary mapping actor ID to scene nodes
        self.actorIDToNode = {}
        
        eventManager = ECOM.eventManager
        eventManager.addListener(self.newRenderComponent, Event_NewRenderComponent.eventType)
        eventManager.addListener(self.actorMoved, Event_ActorMoved.eventType)
        eventManager.addListener(self.screenResize, Event_ScreenResize.eventType)
        eventManager.addListener(self.playAnimation, Event_PlayAnimation.eventType)
        eventManager.addListener(self.destroyActor, Event_DestroyActor.eventType)
        
    def cleanUp(self):
        eventManager = ECOM.eventManager
        eventManager.removeListener(self.newRenderComponent, Event_NewRenderComponent.eventType)
        eventManager.removeListener(self.actorMoved, Event_ActorMoved.eventType)
        eventManager.removeListener(self.screenResize, Event_ScreenResize.eventType)
        eventManager.removeListener(self.playAnimation, Event_PlayAnimation.eventType)
        eventManager.removeListener(self.destroyActor, Event_DestroyActor.eventType)
    
    def findNode(self, actorID):
        if actorID in self.actorIDToNode.keys():
            return self.actorIDToNode[actorID]
        
        return None
    
    def addNode(self, actorID, child):
        self.actorIDToNode[actorID] = child
        
        self.rootNode.addChild(child)
    
    def attachAtNode(self, actorID, node):
        self.actorIDToNode[node.actorID] = node
        parentNode = self.findNode(actorID)
        parentNode.addChild(node)
        
    def render(self):
        self.viewRect = self.camera.viewRect
        self.rootNode.render(self)
        
    def newRenderComponent(self, event):
        if event.toParent:
            self.attachAtNode(event.actorID, event.sceneNode)
        else:
            self.addNode(event.actorID, event.sceneNode)
    
    def actorMoved(self, event):
        node = self.findNode(event.actorID)
        if node is not None:
            node.setPosition(event.pos)
            node.setRotation(event.angle)
   
    def destroyActor(self, event):
        self.rootNode.removeChild(event.actorID)
        del self.actorIDToNode[event.actorID]
    
    def screenResize(self, event):
        self.camera.resizeViewRect(event.width, event.height)
    
    def playAnimation(self, event):
        node = self.actorIDToNode[event.actorID]
        
        if hasattr(node, 'animation'):
            if node.name == event.name:
                node.playAnimation()
        else:
            for child in node.children:
                if hasattr(child, 'animation'):
                    if child.name == event.name:
                        child.playAnimation()


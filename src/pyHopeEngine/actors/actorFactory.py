'''
Created on Jun 21, 2013

@author: Devon

Defines ActorFactory to create actors
'''

import xml.etree.ElementTree as ET

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.actors.components import *
from pyHopeEngine import Actor


class ActorFactory(object):
    '''Uses XML files to create game actors'''
    
    def __init__(self):
        self.lastActorID = 0
        
        #Dictionary of all components
        self.componentDict = {"SpriteRenderComponent":              renderComponent.SpriteRenderComponent,
                              "LineSegmentRenderComponent":         renderComponent.LineSegmentRenderComponent,
                              "ShapeRenderComponent":               renderComponent.ShapeRenderComponent,
                              "HealthBarRenderComponent":           renderComponent.HealthBarRenderComponent,
                              "PhysicsComponent":                   physicsComponent.PhysicsComponent,
                              "ConstantVelocityPhysicsComponent":   physicsComponent.ConstantVelocityPhysicsComponent,
                              "TransformComponent":                 transformComponent.TransformComponent,
                              "HealthComponent":                    healthComponent.HealthComponent,
                              "AnimationComponent":                 animationComponent.AnimationComponent,
                              "ChildActorsComponent":               childActorsComponent.ChildActorsComponent}
        
    def createActor(self, resource, initialPos = None, actorID = None, parent = None):
        '''Creates an actor from a given resource.
        
        Keyword arguments:
            resource -- file defining the actor
            actorID -- unique ID to associate with actor
        '''
        
        resource = ECOM.engine.resourceManager.getFile(resource)
        xmlTree = ET.ElementTree(file = resource)
        if actorID is None:
            actorID = self.lastActorID
            self.lastActorID += 1  
             
        actor = Actor(actorID)
        actor.init(xmlTree.getroot())
        
        for element in xmlTree.iter():
            if element.tag not in self.componentDict:
                continue
            
            component = self.createComponent(element)
            actor.addComponent(component)
            component.owner = actor
        
        transformComp = actor.getComponent('TransformComponent')
        if initialPos and transformComp:
            transformComp.pos = initialPos
        
        actor.parent = parent
        actor.postInit()
        return actor
    
    def createComponent(self, element):
        component = self.componentDict[element.tag]()
        component.init(element)
        
        return component
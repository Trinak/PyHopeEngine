'''
Created on Jun 21, 2013

@author: Devon

Defines rendering components
'''

import pygame

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.graphics.sceneNode import SpriteNode, LineSegmentNode, ShapeNode, HealthBarNode
from pyHopeEngine.actors.components.actorComponent import ActorComponent
from pyHopeEngine import Event_NewRenderComponent


class RenderComponent(ActorComponent):
    '''Base render component'''
    
    def __init__(self):
        self.name = "RenderComponent"
        self.owner = None
        self.color = None
        self.sceneNode = None

    def init(self, element):
        ''' Initializes the component from an XML file
        
        Keyword arguments:
            element - the XML node containing this component
        '''
        
        colorElement = element.find("Color")
        
        if colorElement is not None:
            self.color = self.findColor(colorElement)
    
    def postInit(self):
        '''Creates the scene node associated with this actor'''
        self.sceneNode = self.createSceneNode()
        event = Event_NewRenderComponent(self.owner.actorID, self.sceneNode)
        ECOM.eventManager.triggerEvent(event)
    
    def findColor(self, element):
        '''Finds the color of the actor or sets to a default color'''
        
        if element is not None:
            r = eval(element.attrib.get("r", "255"))
            g = eval(element.attrib.get("g", "255"))
            b = eval(element.attrib.get("b", "255"))
            a = eval(element.attrib.get("a", "255"))
        else:
            r = 255
            g = 255
            g = 255
            a = 255
        
        return pygame.Color(r, g, b, a)
    
    def createSceneNode(self):
        '''Implemented by subclasses to create the correct scene node'''
        raise NotImplementedError(self.name + ": createSceneNode not implemented.")
    
    
class SpriteRenderComponent(RenderComponent):
    '''Creates sprites and sprite nodes'''
    
    def __init__(self):
        super().__init__()
        self.spriteFile = None
    
    def init(self, element):
        ''' Initializes the component from an XML file
        
        Keyword arguments:
            element - the XML node containing this component
        '''
        
        spriteElement = element.find("Sprite")
        if spriteElement is not None:
            self.spriteFile = spriteElement.text
    
    def createSceneNode(self):
        '''Creates the sprite node and sets its position in the world'''
        transformComponent = self.owner.getComponent("TransformComponent")
        
        if transformComponent.pos is not None:
            pos = transformComponent.pos
            direction = transformComponent.direction
        else:
            pos = (0, 0)
            direction = (0, 1)
            
        sceneNode = SpriteNode(self.owner.actorID, self, pos, direction, self.spriteFile)
        
        return sceneNode


class LineSegmentRenderComponent(RenderComponent):
    def __init__(self):
        super().__init__()
    
    def createSceneNode(self):
        '''Creates the line segment node and sets its position in the world'''
        physicsComponent = self.owner.getComponent("TransformComponent")
        
        if physicsComponent is not None:
            vertices = physicsComponent.properties.vertices
            thickness = physicsComponent.properties.thickness
        else:
            vertices = ((0, 0), (1, 1))
        
        sceneNode = LineSegmentNode(self.owner.actorID, self, vertices, self.color, thickness)
        
        return sceneNode


class ShapeRenderComponent(RenderComponent):
    def __init__(self):
        super().__init__()
    
    def init(self, element):
        ''' Initializes the component from an XML file
        
        Keyword arguments:
            element - the XML node containing this component
        '''
        
        super().init(element)
        
        shapeElement = element.find('Shape')
        if shapeElement is not None:
            self.shape = shapeElement.text
        else:
            self.shape = 'rect'
        
        widthElement = element.find('Width')
        if widthElement is not None:
            self.width = eval(widthElement.text)
        else:
            self.width = 1
    
    def createSceneNode(self):
        '''Creates the shape node and sets its position in the world'''
        transformComponent = self.owner.getComponent("TransformComponent")
        
        if transformComponent is not None:
            pos = transformComponent.pos
            size = transformComponent.size
        else:
            pos = (0, 0)
            size = (10, 10)
        
        sceneNode = ShapeNode(self.owner.actorID, self, self.shape, pos, size, self.color, self.width)
        
        return sceneNode


class HealthBarRenderComponent(RenderComponent):
    def __init__(self):
        super().__init__()
        self.value = None
        self.minValue = None
        self.maxValue = None
        
    def init(self, element):
        ''' Initializes the component from an XML file
        
        Keyword arguments:
            element - the XML node containing this component
        '''
        valueEle = element.find("Value")
        self.value = eval(valueEle.text)
        
        minEle = element.find("MinValue")
        self.minValue = eval(minEle.text)
        
        maxEle = element.find("MaxValue")
        self.maxValue = eval(maxEle.text)
    
    def createSceneNode(self):
        '''Creates the health bar UI node'''
        transformComponent = self.owner.getComponent("TransformComponent")
        
        if transformComponent is not None:
            pos = transformComponent.pos
            size = transformComponent.size
        
        rect = (pos, size)
        sceneNode = HealthBarNode(self.owner.actorID, self, rect, self.value, self.minValue, self.maxValue)
        
        return sceneNode
        
        
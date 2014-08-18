'''
Created on Jun 13, 2013

@author: Devon

Defines various scene nodes
'''

import math
import pygame
import pyganim

from pymunk import Vec2d
from pyHopeEngine.graphics.sprite import GameSprite
from pyHopeEngine.userInterface.healthBar import HealthBar

class SceneNode(object):
    '''Base scene node'''
    
    def __init__(self, actorID, renderComponent):
        '''Creates a new scene node
        
        Keyword arguments:
            actorID -- ID of the represented actor
            renderComponent -- render component of the actor
        '''
        self.actorID = actorID
        self.renderComp = renderComponent
        self.children = []
        self.parent = None
        self.direction = None
        self.rect = None
    
    def addChild(self, child):
        '''Adds a child to the node'''
        self.children.append(child)
        child.parent = self
    
    def render(self):
        pass
    
    def renderChildren(self, scene):
        for child in self.children:
            child.render(scene)
    
    def removeChild(self, actorID):
        for child in list(self.children):
            if child.actorID == actorID:
                self.children.remove(child)          

    def setPosition(self, pos):
        pass
    
    def setRotation(self, angle):
        pass


class RootNode(SceneNode):
    '''Root node of the scene'''
    
    def __init__(self):
        super().__init__(None, None)
    
    def render(self, scene):
        self.renderChildren(scene)


class CameraNode(SceneNode):
    '''Camera node of the scene'''
    
    def __init__(self, width, height):
        '''Create a new camera
        
        Keyword arguments:
            width -- width of the viewable area
            height -- height of the viewable area
        '''
        self.viewRect = pygame.Rect(0, 0, width, height)
        self.target = None
    
    def setTarget(self, target):
        '''Sets the target of the camera'''
        self.target = target
    
    def resizeViewRect(self, width, height):
        '''Changes the size of the viewable area'''
        self.viewRect.width = width
        self.viewRect.height = height


class RectNode(SceneNode):
    '''Uses rect for boundary. Use subclasses to specialize'''
    
    def __init__(self, actorID, renderComponent):
        super().__init__(actorID, renderComponent)
        self.rect = None
    
    def isOnScreen(self, area, viewPos):
        '''Determines if the node is in the viewable area'''
        if viewPos.left > area.right:
            return False
        
        if viewPos.right < area.left:
            return False
        
        if viewPos.top > area.bottom:
            return False
        
        if viewPos.bottom < area.top:
            return False
        
        return True
    
    def setPosition(self, pos):
        '''Sets the nodes position'''
        self.rect.centerx = pos.x
        self.rect.centery = pos.y
    
    def setRotation(self, angle):
        pass
        

class SpriteNode(RectNode):
    '''Node to hold sprite images'''
    
    def __init__(self, actorID, renderComponent, pos, rotation, file):
        '''Create a new sprite node
        
        Keyword arguments:
            actorID -- ID of the represented actor
            renderComponent -- render component of the actor
            pos -- initial position of the sprite
            file -- file of the sprite image
        '''
        super().__init__(actorID, renderComponent)
        self.addSpriteImage(file, pos, rotation)
    
    def addSpriteImage(self, file, pos, rotation):
        self.sprite = GameSprite(file)
        self.rect = self.sprite.image.get_rect()
        self.rect.centerx = pos.x
        self.rect.centery = pos.y
        self.initRotation = rotation
        self.rotation = rotation
        self.initWidth = self.rect.width
        self.initHeight = self.rect.height
    
    def render(self, scene):
        viewPos = self.rect.move(scene.viewRect.topleft)
        
        if self.isOnScreen(scene.viewRect, viewPos):
            scene.renderer.render(self.sprite.image, viewPos)
            
            for child in self.children:
                child.render(scene)
    
    def setRotation(self, angle):
        self.rotation = angle
        rotate = self.initRotation - angle 
        rotate = math.degrees(rotate)
        self.sprite.image = pygame.transform.rotozoom(self.sprite.oriImage, rotate, 1)
        self.rect = self.sprite.image.get_rect(center = self.rect.center)


class ShapeNode(RectNode):
    '''Node to display basic shapes'''
    
    def __init__(self, actorID, renderComponent, shape, pos, size, color, width):
        '''Create a new shape node
        
        Keyword arguments:
            actorID -- ID of the represented actor
            renderComponent -- render component of the actor
            pos -- initial center position of the shape
            size -- either a tuple of (width, height) or a radius
            color -- color of the shape
            width -- width of the shape lines, 0 is filled
        '''
        
        super().__init__(actorID, renderComponent)
        self.shape = shape
        self.size = size
        self.color = color
        self.width = width
        self.rect = None
        self.image = None
        self.oriImage = None
        
        self.setImage()
        self.rect.centerx = pos.x
        self.rect.centery = pos.y
    
    def setImage(self):
        '''Draw the shape onto a surface'''
        if self.shape == 'rect':
            self.rect = pygame.Rect((0, 0), self.size)
            self.oriImage = pygame.Surface((self.rect.width * 2, self.rect.height * 2))
            pygame.draw.rect(self.oriImage, self.color, self.rect, self.width)
        elif self.shape == 'circle':
            self.rect = pygame.Rect((0, 0), self.size * 2, self.size * 2)
            self.oriImage = pygame.Surface((self.rect.width, self.rect.height))
            pygame.draw.circle(self.oriImage, self.color, self.rect.center, self.size, self.width)
        
        self.image = self.oriImage.copy()
    
    def render(self, scene):
        viewPos = self.rect.move(scene.viewRect.topleft)
        
        if self.isOnScreen(scene.viewRect, viewPos):
            scene.renderer.render(self.image, self.rect)
            
            for child in self.children:
                child.render(scene)
    
    def setRotation(self, angle):
        self.image = pygame.transform.rotozoom(self.oriImage, angle, 1)
        self.rect = self.image.get_rect(center = self.rect.center)
   

class AnimationNode(RectNode):      
    def __init__(self, actorID, renderComponent, frames, loop, rect, direction, name):
        super().__init__(actorID, renderComponent)
        self.animation = pyganim.PygAnimation(frames, loop)
        self.rect = rect
        self.name = name
        self.initDirection = Vec2d(direction)
    
    def render(self, scene):
        surf = scene.renderer.displaySurface
        self.animation.blit(surf, self.rect)
        self.animation.clearTransforms()
    
    def playAnimation(self):
        self.animation.play()
    
    def rotate(self, angle):
        self.animation.rotate(angle)
    
    def getTransformedRect(self, index, **kwargs):
        '''Returns a rect using pygames Surface get_rect method'''
        return self.animation._transformedImages[index].get_rect(**kwargs)
        

class LineSegmentNode(SceneNode):
    '''Represents a single line segment'''
    
    def __init__(self, actorID, renderComponent, vertices, color, width):
        '''Creates a new line segment node
        
        Keyword arguments:
            actorID -- ID of the represented actor
            renderComponent --- render component of the actor
            vertices -- list of the two endpoints
            color -- color of the line
            width -- width of the line
        '''
        
        super().__init__(actorID, renderComponent)
        self.pointOne = Vec2d(vertices[0])
        self.pointTwo = Vec2d(vertices[1])
        self.color = color
        self.width = width   
    
    def render(self, scene):
        viewPosA = self.pointOne + Vec2d(scene.viewRect.topleft)
        viewPosB = self.pointTwo + Vec2d(scene.viewRect.topleft)
        if self.isOnScreen(scene.viewRect, viewPosA, viewPosB):
            scene.renderer.renderLine(self.color, viewPosA, viewPosB, self.width)
        
            for child in self.children:
                child.render(scene)           
            
    def isOnScreen(self, area, viewPosA, viewPosB):
        '''Determines if the line is onScreen'''
        if self.pointInRect(viewPosA, area):
            return True
        
        if self.pointInRect(viewPosB, area):
            return True
        
        topLeft = Vec2d(area.topleft)
        topRight = Vec2d(area.topright)
        bottomLeft = Vec2d(area.bottomleft)
        bottomRight = Vec2d(area.bottomright)
        
        return (self.lineInterLine(viewPosA, viewPosB, topLeft, topRight) or
                self.lineInterLine(viewPosA, viewPosB, topRight, bottomRight) or
                self.lineInterLine(viewPosA, viewPosB, bottomRight, bottomLeft) or
                self.lineInterLine(viewPosA, viewPosB, bottomLeft, topRight))
    
    def pointInRect(self, point, rect):
        '''Returns True if a point is inside a rectangle'''
        if (point.x > rect.left and point.x < rect.right and
            point.y > rect.top and point.y < rect.bottom):
            return True
        else:
            return False
    
    def lineInterLine(self, ptOneA, ptTwoA, ptOneB, ptTwoB):
        '''Returns True if two lines intersect'''
        top = (ptOneA.y - ptOneB.y) * (ptTwoB.x - ptOneB.x) - (ptOneA.x - ptOneB.x) * (ptTwoB.y - ptOneB.y)
        bottom = (ptTwoA.x - ptOneA.x) * (ptTwoB.y - ptOneB.y) - (ptTwoA.y - ptOneA.y) * (ptTwoB.x - ptOneB.x)
        
        if bottom == 0:
            return False
        
        temp = top / bottom
        
        top = (ptOneA.y - ptOneB.y) * (ptTwoA.x -ptOneA.x) - (ptOneA.x - ptOneB.x) * (ptTwoA.y - ptOneA.y)
        temp2 = top / bottom
        
        if (temp < 0 or temp > 1 or temp2 < 0 or temp2 > 1):
            return False
        
        return True
    

class HealthBarNode(SceneNode):
    def __init__(self, actorID, renderComponent, rect, value, minValue, maxValue, **params):
        super().__init__(actorID, renderComponent)
        self.UI = HealthBar(rect, value, minValue, maxValue, **params)
    
    def render(self):
        self.UI.render()
        
            
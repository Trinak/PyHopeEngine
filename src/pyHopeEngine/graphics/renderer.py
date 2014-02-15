'''
Created on Jun 4, 2013

@author: Devon

Defines the main rendering system
'''

import pygame

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Event_ScreenResize

class Renderer:
    '''Main renderer'''
    
    def __init__(self):
        self.displaySurface = None
        self.flags = 0
    
    def cleanUp(self):
        ECOM.eventManager.removeListener(self.screenResize, Event_ScreenResize.eventType)
           
    def initMainSurface(self, caption, flags = 0):
        '''Initializes the main display surface.
        
        Keyword arguments:
            caption -- caption of the window
            flags -- pygame display flags (ie FULLSCREEN, RESIZABLE, etc)
        '''
        self.flags = flags
        self.displaySurface = pygame.display.set_mode((ECOM.Screen.windowWidth, ECOM.Screen.windowHeight), self.flags)
        pygame.display.set_caption(caption)
        ECOM.eventManager.addListener(self.screenResize, Event_ScreenResize.eventType)
    
    def clearSurface(self, color):
        '''Fills surface with given color'''
        self.displaySurface.fill(color)
    
    def render(self, image, pos):
        self.displaySurface.blit(image, pos)
    
    def renderShape(self, shape, color, points, radius = None, width = 0,):
        '''Renders a shape to the main surface
        
        Keyword arguments:
            shape -- string type of shape (rect, circle, or poly)
            color -- color of shape
            points -- a rect for rect, center pos for circle, points for poly
            radius -- radius of a circle
            width -- width of lines, 0 means fill
        '''
        
        surface = self.displaySurface
            
        if shape == 'rect':
            rect = pygame.Rect(points)
            pygame.draw.rect(surface, color, rect, width)
        elif shape == 'circle':
            pygame.draw.circle(surface, color, points, radius, width=0)
        elif shape == 'poly':
            pygame.draw.polygon(surface, color, points, width)
    
    def renderLine(self, color, startPos, endPos, width = 1):
        pygame.draw.line(self.displaySurface, color, startPos, endPos, width)
        
    def renderLines(self, color, points, closed = True, width = 1):
        '''Render a group of lines
        
        Keyword arguments:
            color -- the pygame color
            points -- list of points
            closed -- if the last point should connect to the first
            width -- width of lines
        '''
        
        pygame.draw.lines(self.displaySurface, color, closed, points, width)
    
    def screenResize(self, event):
        '''Updates the width and height of the display screen'''
        ECOM.Screen.updateWidth(event.width)
        ECOM.Screen.updateHeight(event.height)
        self.displaySurface = pygame.display.set_mode((ECOM.Screen.windowWidth, ECOM.Screen.windowHeight), self.flags)
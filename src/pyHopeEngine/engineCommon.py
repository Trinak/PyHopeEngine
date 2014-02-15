'''
Created on Jun 21, 2013

@author: Devon

Global access point for modules.
'''

from pygame import Color

#Colors
class Colors:
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    GRAY = Color(128, 128, 128)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    TEAL = Color(0, 128, 128)
    OLIVE = Color(128, 128, 0)
    PURPLE = Color(128, 0, 128)
    SILVER = Color(192, 192, 192)
    

class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class Screen:
    windowWidth = 1280
    windowHeight = 800
    
    @classmethod
    def updateWidth(cls, width):
        Screen.windowWidth = width
    
    @classmethod
    def updateHeight(cls, height):
        Screen.windowHeight = height
    
    @ClassProperty    
    @classmethod
    def halfW(cls):
        return Screen.windowWidth / 2
     
    @ClassProperty
    @classmethod
    def thirdW(cls):
        return Screen.windowWidth / 3
    
    @ClassProperty
    @classmethod
    def fourthW(cls):
        return Screen.windowWidth / 4
    
    @ClassProperty
    @classmethod
    def halfH(cls):
        return Screen.windowHeight / 2

    @ClassProperty
    @classmethod
    def thirdH(cls):
        return Screen.windowHeight / 3
    
    @ClassProperty
    @classmethod
    def fourthH(cls):
        return Screen.windowHeight / 4


class Debug:
    TABLE = False
    PHYSICS = False


engine = None
eventManager = None
animationManager = None
actorManager = None


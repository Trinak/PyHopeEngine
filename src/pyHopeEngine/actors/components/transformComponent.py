'''
Created on Oct 3, 2013

@author: Devon Arrington
'''

from pyHopeEngine import Vec2d
from pyHopeEngine.actorComponent import ActorComponent


class TransformComponent(ActorComponent):
    def __init__(self):
        self.name = "TransformComponent"
        self.owner = None
        self.direction = None
        self.pos = None
        self.angle = None
        
        #size is (width, height)
        self.size = None
        
    def init(self, element):
        '''Initialize the component from a given XML file.
        
        Keyword arguments:
            element -- the XML node containing this component
        '''
        
        directElement = element.find("Direction")
        if directElement is not None:
            self.direction = Vec2d(eval(directElement.text))
            self.direction.normalized()
        else:
            self.direction = Vec2d(1, 0)
        
        posElement = element.find("Position")
        if posElement is not None:
            self.pos = Vec2d(eval(posElement.text))
        else:
            self.pos = (0, 0)
        
        sizeElement = element.find("Size")
        if sizeElement is not None:
            self.size = eval(sizeElement.text)
        else:
            self.size = (1, 1)
            
    def postInit(self):
        pass


class SubTransformComponent(TransformComponent):
    '''Transform with position based on a parent'''
    def __init__(self):
        super().__init()
        self.offset = Vec2d((0, 0))
    
    def init(self, element):
        super().init(element)
        
        offsetElement = element.find("Offset")
        self.offset = eval(offsetElement.text)
        
        self.pos += self.offset
        
        
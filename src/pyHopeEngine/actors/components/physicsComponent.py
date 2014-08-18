'''
Created on Jul 17, 2013

@author: Devon

Defines basic actor physics components
'''

import pymunk

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Vec2d
from pyHopeEngine.actors.components.actorComponent import ActorComponent

infinity = pymunk.inf
Screen = ECOM.Screen

class PhysicsProperties(object):
    '''Class to hold properties'''
    
    def __init__(self):
        self.mass = 1
        self.moment = 1
        self.shapeType = None
        self.acceleration = 0
        self.angularAcceleration = 0
        self.elasticity = 0
        self.collisionType = 0
        self.velocityLimit = 0
        self.isStatic = False
        
        #Either the 2 points in line or vertices of a poly
        self.vertices = None
        self.thickness = None
        

class PhysicsComponent(ActorComponent):
    '''Base physics component'''
        
    def __init__(self):
        self.name = "PhysicsComponent"
        self.properties = PhysicsProperties()
        self.owner = None
        self.physics = None
    
    def init(self, element):
        '''Initialize the component from a given XML file.
        
        Keyword arguments:
            element -- the XML node containing this component
        '''
        
        self.physics = ECOM.engine.baseLogic.physics
        self.setProperties(element)
    
    def setProperties(self, element):
        '''Sets the physical properties of the component.
        
        Keyword arguments:
            element - same element from init
        '''
        
        self.properties.mass = self.findProperty(element, "Mass", None)
        self.properties.moment = self.findProperty(element, "Moment", None)
        self.properties.shapeType = self.findProperty(element, "Shape", "Circle", False)
        self.properties.elasticity = self.findProperty(element, "Elasticity", 0.0)
        self.properties.collisionType = self.findProperty(element, "CollisionType", 0)
        self.properties.velocityLimit = self.findProperty(element, "VelocityLimit", pymunk.inf)
        self.properties.isStatic = self.findProperty(element, "IsStatic", False)
        self.properties.vertices = self.findProperty(element, "Vertices", None)
        self.properties.thickness = self.findProperty(element, "Thickness", 1)
    
    def findProperty(self, mainElement, name, default, evaluate = True):
        '''Finds the element containing the property and returns the value.
        
        Keyword arguments:
            mainElement -- the main element passed to init
            name -- the name of the desired property node
            default -- the default value to return if node is not found
            evaluate -- used to either evaluate the text or return as string
        '''
        
        element = mainElement.find(name)
        
        if element is not None:
            if evaluate:
                prop = eval(element.text)
            else:
                prop = element.text
        else:
            prop = default

        return prop    
    
    def update(self):
        transformComponent = self.owner.getComponent("TransformComponent")
        direction = transformComponent.direction
        
        if self.properties.acceleration != 0:
            self.physics.applyImpulse(self.owner.actorID, direction, self.properties.acceleration)
        
        if self.properties.angularAcceleration != 0:
            self.physics.changeAngle(self.owner.actorID, self.properties.angularAcceleration)
            
    def setCollisionType(self, num):
        '''Sets the collision number of the corresponding shape.'''
        self.physics.setCollisionType(self.owner.actorID, num)
    
    def applyAcceleration(self, acceleration):
        self.properties.acceleration = acceleration
    
    def removeAcceleration(self):
        self.properties.acceleration = 0
    
    def applyAngularAcceleration(self, acceleration):
        self.properties.angularAcceleration = acceleration
    
    def removeAngularAcceleration(self):
        self.properties.angularAcceleration = 0
        
    def applyImpulse(self, direction, magnitude):
        self.physics.applyImpulse(self.owner.actorID, direction, magnitude)
    
    def setVelocity(self, velocity):
        velocity = Vec2d(velocity)
        self.physics.setVelocity(self.owner.actorID, velocity)
        
    def cleanUp(self):
        '''Removes the body and shape from the physics system.'''
        self.physics.removeObjects(self.owner.actorID)
            
    def postInit(self):
        '''Actually creates the body and shape in the physics system.'''
        transformComponent = self.owner.getComponent("TransformComponent")
        pos = transformComponent.pos
        size = transformComponent.size
        rotation = transformComponent.rotation
    
        if self.properties.shapeType == "Circle":
            size = size[0] / 2
            self.physics.addCircle(self.owner.actorID, pos = pos, size = size, **self.properties.__dict__)
            
        elif self.properties.shapeType == "Box":
            self.physics.addBox(self.owner.actorID, pos = pos, size = size, **self.properties.__dict__)
            
        elif self.properties.shapeType == "Poly":
            self.physics.addPoly(self.owner.actorID, pos = pos, size = size, **self.properties.__dict__)
            
        elif self.properties.shapeType =="Segment":
            self.physics.addSegment(self.owner.actorID, pos = pos, size = size, **self.properties.__dict__)
        
        self.physics.setDirection(self.owner.actorID, rotation)
        self.physics.setVelocityLimit(self.owner.actorID, self.properties.velocityLimit)


class ConstantVelocityPhysicsComponent(PhysicsComponent):
    '''A physics component that has a constant velocity.'''
    
    def __init__(self):
        super().__init__()
        self.startVelocityMod = None
        self.velocityMod = None
        
    def init(self, element):
        '''Initialize the component from a given XML file.
        
        Keyword arguments:
            element -- the XML node containing this component
        '''
        
        super().init(element)
        self.startVelocityMod = self.findProperty(element, "VelocityMod", 100)
        self.velocityMod = self.startVelocityMod
   
    def postInit(self):
        '''Actually creates the body and shape in the physics system.
        Also applys a starting impulse and sets a constant velocity.
        '''
        super().postInit()
        
        transformComponent = self.owner.getComponent("TransformComponent")
        direction = transformComponent.direction
        
        self.physics.applyImpulse(self.owner.actorID, direction, self.velocityMod)
        self.setConstantVelocity(self.velocityMod)

    def changeVelocityMod(self, newMod):
        self.velocityMod = newMod
        self.setConstantVelocity(self.velocityMod)

    def setConstantVelocity(self, mod):
        '''Sets the function for the physics system to use
        for the constant velocity.
        
        Keyword arguments:
            mod - the number to multiply the velocity by
        '''
        
        def constantVelocity(body, gravity, damping, dt):
            '''Provides a constant velocity'''
            body.velocity = body.velocity.normalized() * mod
        
        self.physics.setVelocityFunc(self.owner.actorID, constantVelocity)

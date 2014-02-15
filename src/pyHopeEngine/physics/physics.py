'''
Created on Jul 19, 2013

@author: Devon

Defines the main physics system
'''

import copy
import math
import pygame
import pymunk
import pymunk.pygame_util

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Event_ActorMoved

class NullPhysics(object):
    '''Null physics for a remote game'''
    def __init__(self):
        pass
    def setGravity(self, gravityX, gravityY):
        pass
    def addShape(self, actorID, body, shape, elasticity, collisionType):
        pass
    def addCircle(self, actorID, **kwargs):
        pass
    def addBox(self, actorID, **kwargs):
        pass
    def addPoly(self, actorID, **kwargs):
        pass
    def addSegment(self, actorID, **kwargs):
        pass    
    def createBody(self, isStatic, mass, moment, pos, angle):
        pass
    def addConstraint(self, constraintType, actorIDA, actorIDB, **kwargs):
        pass
    def getBody(self, actorID, shapeID = 0):
        pass
    def removeObjects(self, actorID):
        pass
    def addCollisionHandler(self, typeOne, typeTwo, begin = None, pre_solve = None, post_solve = None, separate = None, *args, **kwargs):
        pass
    def linkActor(self, actorID, shape):
        pass
    def update(self, time):
        pass
    def syncWithGraphics(self):
        pass
    def changeVelocity(self, actorID, velocity):
        pass
    def changeRotation(self, actorID, angle):
        pass
    def applyForce(self, actorID, force, offset = (0, 0)):
        pass
    def applyImpulse(self, actorID, impulse, offset = (0, 0)):
        pass
    def setCollisionType(self, actorID, num):
        pass
    def setVelocityFunc(self, actorID, func):
        pass
    def debugDraw(self, screen):
        pass
    def debugOutlineColor(self, shape, color):
        pass
    
    
class PhysicsManager(object):
    '''Main physics system'''
    
    def __init__(self):
        self.lastGroupID = 1
        self.space = pymunk.Space()
        self.actorIDToShape = {}
        self.shapeToActorID = {}
        self.constraintDict = {"DampedRotarySpring":    pymunk.DampedRotarySpring,
                               "DampedSpring":          pymunk.DampedSpring,
                               "GearJoint":             pymunk.GearJoint,
                               "GrooveJoint":           pymunk.GrooveJoint,
                               "PinJoint":              pymunk.PinJoint,
                               "PivotJoint":            pymunk.PivotJoint,
                               "RatchetJoint":          pymunk.RatchetJoint,
                               "RotaryLimitJoint":      pymunk.RotaryLimitJoint,
                               "SimpleMotor":           pymunk.SimpleMotor,
                               "SlideJoint":            pymunk.SlideJoint}
        
    
    def setGravity(self, gravityX, gravityY):
        '''Set the worlds gravity'''
        self.space.gravity = (gravityX, gravityY)
    
    def setDamping(self, damping):
        '''Sets how fast objects lose velocity, 1.0 is no damping'''
        self.space.damping = damping
    
    def addShape(self, actorID, body, shape, elasticity, collisionType):
        '''Adds a shape and its body to the physics system'''
        shape.elasticity = elasticity
        shape.collision_type = collisionType
        
        if ECOM.Debug.PHYSICS:
            self.debugOutlineColor(shape, ECOM.Colors.RED)
        
        if body == self.space.static_body:
            self.space.add(shape)
        else:
            self.space.add(body, shape)
        
        if actorID is not None: 
            self.linkActor(actorID, shape)
    
    def addCircle(self, actorID, **kwargs):
        '''Create a circle shape and body'''
        if kwargs['moment'] == -1:
            kwargs['moment'] = pymunk.moment_for_circle(kwargs['mass'], 0, kwargs['size'])
            
        body = self.createBody(kwargs['isStatic'], kwargs['mass'], kwargs['moment'], kwargs['pos'])
        shape = pymunk.Circle(body, kwargs['size'])
        self.addShape(actorID, body, shape, kwargs['elasticity'], kwargs['collisionType'])
    
    def addBox(self, actorID, **kwargs):
        '''Create a box shape and body'''
        if kwargs['moment'] == -1:
            kwargs['moment'] = pymunk.moment_for_box(kwargs['mass'], kwargs['size'][0], kwargs['size'][1])
            
        body = self.createBody(kwargs['isStatic'], kwargs['mass'], kwargs['moment'], kwargs['pos'])
        shape = pymunk.Poly.create_box(body, kwargs['size'])
        self.addShape(actorID, body, shape, kwargs['elasticity'], kwargs['collisionType'])
    
    def addPoly(self, actorID, **kwargs):
        '''Create a polygon shape and body'''
        if kwargs['moment'] == -1:
            kwargs['moment'] = pymunk.moment_for_poly(kwargs['mass'], kwargs['vertices'])
            
        body = self.createBody(kwargs['isStatic'], kwargs['mass'], kwargs['moment'], kwargs['pos'])
        shape = pymunk.Poly(body, kwargs['vertices'])
        self.addShape(actorID, body, shape, kwargs['elasticity'], kwargs['collisionType'])
    
    def addSegment(self, actorID, **kwargs):
        '''Create a line segment shape and body'''
        if kwargs['moment'] == -1:
            kwargs['moment'] = pymunk.moment_for_segment(kwargs['mass'], kwargs['vertices'][0], kwargs['vertices'][1])
        
        body = self.createBody(kwargs['isStatic'], kwargs['mass'], kwargs['moment'], kwargs['pos'])
        shape = pymunk.Segment(body, kwargs['vertices'][0], kwargs['vertices'][1], kwargs['thickness'])
        self.addShape(actorID, body, shape, kwargs['elasticity'], kwargs['collisionType'])
    
    def createBody(self, isStatic, mass, moment, pos):
        '''Creates a physics body'''
        if isStatic:
            body = self.space.static_body
        else:
            body = pymunk.Body(mass, moment)
            body.position = pos       

        return body
    
    def setDirection(self, actorID, angle):
        body = self.getBody(actorID)
        body.angle = angle
    
    def setPosition(self, actorID, pos):
        body = self.getBody(actorID)
        body.position = pos
        
    def setVelocityLimit(self, actorID, limit):
        body = self.getBody(actorID)
        body.velocity_limit = limit
    
    def addConstraint(self, constraintType, actorIDA, actorIDB, **kwargs):
        '''Adds a constraint to two objects'''
        if actorIDA == None:
            bodyA = self.space.static_body
        else:
            bodyA = self.getBody(actorIDA)
            
        if actorIDB == None:
            bodyB = self.space.static_body
        else:
            bodyB = self.getBody(actorIDB)
            
        constraint = self.constraintDict[constraintType](bodyA, bodyB, **kwargs)
        self.space.add(constraint)
    
    def getActorID(self, shape):
        '''Returns the actorID of a shape'''
        return self.shapeToActorID[shape]
    
    def getShape(self, actorID):
        '''Returns the shape attached to the ID'''
        return self.actorIDToShape[actorID]
    
    def getBody(self, actorID):
        '''Returns the actors physics body'''
        return self.actorIDToShape[actorID].body
    
    def getVelocity(self, actorID):
        return self.getBody(actorID).velocity
    
    def removeObjects(self, actorID):
        '''Remove objects from the physics system'''
        shape = self.actorIDToShape[actorID]
        body = shape.body
        if body is not self.space.static_body:
            self.space.remove(body, shape, body.constraints)
        else:
            self.space.remove(shape)
        
        del self.actorIDToShape[actorID]
        
    def addCollisionHandler(self, typeOne, typeTwo, begin = None, pre_solve = None, post_solve = None, separate = None, *args, **kwargs):
        '''Add a collision handler between two types'''
        self.space.add_collision_handler(typeOne, typeTwo, begin, pre_solve, post_solve, separate, *args, **kwargs)
    
    def linkActor(self, actorID, shape):
        '''Links an actors ID to its shape'''
        if actorID not in self.actorIDToShape:
            self.actorIDToShape[actorID] = shape
            self.shapeToActorID[shape] = actorID
    
    def update(self, time):
        self.space.step(time)
        
    def syncWithGraphics(self):
        '''Syncs objects positons in the physics system with the graphics system'''
        for actorID, shape in self.actorIDToShape.items():
            body = shape.body
            actor = ECOM.engine.baseLogic.actorManager.findActor(actorID)
            transComp = actor.getComponent("TransformComponent")
            if transComp.pos != body.position or transComp.direction.angle != body.angle:
                transComp.pos = copy.copy(body.position)
                transComp.direction.angle = copy.copy(body.angle)    
                transComp.direction.normalized()
                
                event = Event_ActorMoved(actorID, body.position, body.angle)
                ECOM.eventManager.queueEvent(event)      
    
    def setVelocity(self, actorID, velocity):
        body = self.getBody(actorID)
        body.velocity = velocity
    
    def setAngularVelocity(self, actorID, velocity):
        body = self.getBody(actorID)
        body.angular_velocity = velocity
    
    def changeAngle(self, actorID, angle):
        body = self.getBody(actorID)
        body.angle += angle
    
    def applyForce(self, actorID, direction, magnitude, offset = (0, 0)):
        body = self.getBody(actorID)
        force = direction * magnitude
        body.apply_force(force, offset)
    
    def applyImpulse(self, actorID, direction, magnitude, offset = (0, 0)):
        body = self.getBody(actorID)
        impulse = direction * magnitude
        body.apply_impulse(impulse, offset)
    
    def setCollisionType(self, actorID, num):
        shape = self.getShape(actorID)
        shape.collision_type = num
    
    def setVelocityFunc(self, actorID, func):
        body = self.getBody(actorID)
        body.velocity_func = func
    
    def addToGroup(self, actorIDAdd, actorIDGroup):
        '''Adds a shape to a collision group'''
        shapeAdd = self.getShape(actorIDAdd)
        shapeGroup = self.getShape(actorIDGroup)
        
        if shapeGroup.group == 0:
            shapeGroup.group = self.lastGroupID
            self.lastGroupID += 1
            
        shapeAdd.group = shapeGroup.group
    
    def debugDraw(self):
        pymunk.pygame_util.flip_y = False
        screen = pygame.display.get_surface()
        pymunk.pygame_util.draw(screen, self.space)
        
    def debugOutlineColor(self, shape, color):
        shape.color = color
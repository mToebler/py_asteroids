"""
Author: Mark Tobler
File: angularvelocity.py
Description: In addition to the class comments below, this is a listing and
discussion of methods & properties. Rather than provide a simple angle to
rotate on each update, this class has other functionality.
Methods:

"""
import math
from velocity import Velocity
from point import Point
import constants

class AngularVelocity(Velocity):
    #static class variables
    MAX_VIABILITY = 1
    MAX_DRAG = .85 # CANNOT BE 0
    MAX_SPIN = 30
    
    """
    This is an experimental class hoping to capture the marriage of velocity
    and rotation. This may be better suited for 3D games; we'll see. 
    AngularVelocity, or AV, makes use of rotation and vector speed. Rotation 
    expressed through an angle in degrees, and speed through velocity.
    An optional Point as focal point can be set to calculate rotation.
    A focal point set to the center of an object simply turns the object,
    while an off center point including outside of the object's radius,
    will cause arc-like swinging around that point (which can have a 
    Velocity or AngularVelocity all of its own, which should have an 
    orbiting effect. fingers x'd)
    """
    def __init__(self, angle=0.0, velocity=Velocity(0,0)):
        super().__init__()
        self._angle = angle
        self.dx = velocity.dx
        self.dy = velocity.dy
        self.focal_point = Point()
        # the momentum in the rotation
        self.delta_angle = 0
        # drag represents the inertia decay of movements. if this is 
        # set to AngularVelocity.MAX_VIABILITY, rotation will have no inertia.
        self._drag = .85
        # percentage by which drag decays from it's maximum each cycle.
        self.decay = 0.05
    
    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        """Angle is off by 90 in asteroids. Correct"""
        # angle = angle + 90
        if angle < 0:
            # convert to a normal angle. Angles start from the x axis
            self._angle = 360 - (math.fabs(angle) % 360)
        else:
            self._angle = angle % 360
    
    @property
    def display_angle(self):
        return (self._angle + 90) % 360    
        
    @property
    def drag(self):
        return self._drag 
    @drag.setter
    def drag(self, drag):
        self._drag = math.fabs(drag) % AngularVelocity.MAX_VIABILITY
    @property
    def viability(self):
        return AngularVelocity.MAX_VIABILITY - self._drag
    
    @classmethod
    def max_twirl(cls):
        return AngularVelocity.MAX_SPIN * (1/AngularVelocity.MAX_DRAG)
        
    def turn(self, degrees):
        """
        In 0g environment, any movements are going to have some inertia 
        to them. Hence, the velocity attached to rotation.
        """
        self.delta_angle = (self.delta_angle + degrees) if (self.delta_angle + degrees) < AngularVelocity.max_twirl() else AngularVelocity.max_twirl()
        self.drag = AngularVelocity.MAX_DRAG
        # self.angle = self.angle + degrees

    def stabilize(self, factor):
        """Studies angular rotation"""
        self.drag = factor

        
    def advance(self):
        """
        Advances angle from one moment to the next by it's angular velocity
        """
        # delta angle is reduced by less and less each iteration that 
        # turn has not been called.
        if abs(self.delta_angle)> 0:
             self.drag *= self.viability 
        self.delta_angle -= (self.delta_angle * self.drag)
        self.angle = self.angle + self.delta_angle
        
#testing
# av = AngularVelocity()
# av.angle = 540
# print(av.angle)
        
#print (AngularVelocity.max_twirl())
        
        
        
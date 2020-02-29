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

class AngularVelocity(Velocity):
    #static class variables
    MAX_VIABILITY = 1
    
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
        # drag represents the inertia decay of movements. if this is 
        # set to AngularVelocity.MAX_VIABILITY, rotation will have no inertia.
        self._drag = 0.05
    
    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        if angle < 0:
            # convert to a normal angle. Angles start from the x axis
            self._angle = 360 - (math.fabs(angle) % 360)
        else:
            self._angle = angle % 360
        
    @property
    def drag(self):
        return self._drag 
    @drag.setter
    def drag(self, drag):
        self._drag = math.fabs(drag) % AngularVelocity.MAX_VIABILITY
    @property
    def viability(self):
        return AngularVelocity.MAX_VIABILITY - self._drag
        
    def turn(self, angle):
        """
        In 0g environment, any movements are going to have some inertia 
        to them. Hence, the velocity attached to rotation.
        """
        self.angle = self.angle + angle
        self.dx = self.viability * math.sin(angle)
        self.dy = self.viability * math.cos(angle)
        
    def advance(self):
        """
        Advances angle from one moment to the next by it's angular velocity
        """
        pass
        #self.angle 
        
#testing
# av = AngularVelocity()
# av.angle = 540
# print(av.angle)
        
        
        
        
"""
File: velocity.py
Author: Mark Tobler

Encapsulates the idea of movement in 2-D space. The rate of change as 
expressed by the change, or delta, in a point (x and y)
  From the UML:
    dx : float
    dy : float
    __init__()
"""
import math

class Velocity:
    def __init__(self, dx=0.0, dy=0.0):
        """ Constructor: defaulting values to 0.0 if none provided"""
        self.dx = dx
        self.dy = dy
    
    def __repr__(self):
        return f'({self.dx}, {self.dy})'
    
    @classmethod
    def velocity_from_speed_angle(cls, speed=0.0, angle=1):
        """
        Factory method: returns a Velocity Object based upon the provided 
                        speed and angle.
        """
        return Velocity(speed * math.cos(angle*math.pi/180), speed * math.sin(angle*math.pi/180))
    
    @property
    def speed(self):
        """
        the magnitude, or speed, of a velocity forms the hypotenuse of the 
        right triangle formed by dx, dy. If squared  and added, the sqroot 
        will be the speed. Thank you Pythagorus.
        """
        return math.sqrt(self.dx * self.dx + self.dy * self.dy)
            
# this is it for now. May use some of the dunder methods for comparing and adding velocities later.

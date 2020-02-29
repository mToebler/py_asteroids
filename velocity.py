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
        return Velocity(speed * math.sin(angle), speed * math.cos(angle))
            
# this is it for now. May use some of the dunder methods for comparing and adding velocities later.

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
        return f'({self.dx}, {self.dy}), magnitude: {self.speed}'
    
    @classmethod
    def velocity_from_speed_angle(cls, speed=0.0, angle=1):
        """
        Factory method: returns a Velocity Object based upon the provided 
                        speed and angle.
        """
        return Velocity(speed * math.cos(angle*math.pi/180), speed * math.sin(angle*math.pi/180))
    
    @classmethod
    def velocity_from_speed_radians(cls, speed=0.0, radians=0.0):
        """
        Factory method: returns a Velocity Object based upon the provided 
                        speed and radians.
        """
        return Velocity(speed * math.cos(radians), speed * math.sin(radians))
    
    @property
    def speed(self):
        """
        the magnitude, or speed, of a velocity forms the hypotenuse of the 
        right triangle formed by dx, dy. If squared  and added, the sqroot 
        will be the speed. Thank you Pythagorus.
        """
        return math.sqrt(math.pow(self.dx, 2) + math.pow(self.dy, 2))
    
    def __add__(self, other):
        return_v = Velocity(self.dx, self.dy)
        if isinstance(other, Velocity):
            return_v.dx = return_v.dx + other.dx
            return_v.dy = return_v.dy + other.dy
        else:
            print(f'Velocity __add__: {other} not an instance of Veloctiy. Nothing added.')
        return return_v
    
    def slow(self, magnitude):
        """Slows velocity by magnitude"""
        # use speed multiplied by magnitude to get new speed, then use 
        # Pythagorean theorem to figure new dx, dy
        if  0 < magnitude < 1:            
            dx = 0
            dy = 0
            new_speed = self.speed * (1 - magnitude)
            if (self.dx != 0 and self.dy != 0):
                dx = new_speed * (math.sqrt(self.dx**2)/math.sqrt(self.dy**2 + self.dx**2)) * self.dx/abs(self.dx)
                dy = new_speed * (math.sqrt(self.dy**2)/math.sqrt(self.dy**2 + self.dx**2)) * self.dy/abs(self.dy)      
            else :                
                dx = new_speed * self.dx
                dy = new_speed * self.dy
            self.dx, self.dy = dx,  dy
            
    @classmethod
    def cosine(cls, degrees):
        """
        Convenience Method.
        Given an angle in degrees, return the cosine value, or the 
        adjacent side/hypotenuse 
        """
        # converting into radians and returning cosine value
        return math.cos(degrees * math.pi/180)
    
    @classmethod
    def sine(cls, degrees):
        """
        Convenience Method.        
        Given an angle in degrees, return the sine value, or the 
        opposite side/hypotenuse 
        """
        # converting into radians and returning sine value
        return math.sin(degrees * math.pi/180)
    
    @classmethod
    def __deepcopy__(cls, velocity):
        lhs = Velocity(velocity.dx, velocity.dy)
        return lhs
        
        
# this is it for now. May use some of the dunder methods for comparing and adding velocities later.

#testing
# v = Velocity(1.1, 1.2)
# v1 = Velocity.__deepcopy__(v)
# assert(v is not v1)
# # print(v, '\n\n', v1)
# # print('equal?', v is v1, v == v1)
# # print(v is v)
# v.dx += 2
# print(v, '\n\n', v1)
# assert(v is not v1)
# # print('equal?', v is v1, v == v1)
# assert(v is not v)

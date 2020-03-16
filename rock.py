"""
File: rock.py
Author: Mark Tobler
Description: Rock is an Abstract Base Class abstracting the common traits 
and abilities of all flying rocks in a 0 gravity 
environment. (abstract) Rock extends Flyer class.
"""
import arcade
import random
import constants
from abc import ABC, abstractmethod
from point import Point
from velocity import Velocity
from flyer import Flyer
from angularvelocity import AngularVelocity

class Rock(Flyer, ABC):
    """
    Rock abstracts the common traits and abilities of flying rocks
    in a 0 gravity environment.
    """
    
    def __init__(self, startPoint=None, startVelocity=None):
        super().__init__()
        #arcade image        
        self.texture = None #arcade.load_texture(None)
        self.spin = 0
        if startPoint is None:            
            self.center = Point(random.random() * constants.SCREEN_WIDTH, random.random() * constants.SCREEN_HEIGHT)
        else:
            self.center = Point(startPoint.x, startPoint.y)
        if startVelocity is not None:
            self.velocity = Velocity(startVelocity.dx, startVelocity.dy)
        self.angle = random.random() * 360
        self.points = 0
    
    # def draw(self):
    #     """
    #     used by extending classes to draw using texture
    #     """
    #     arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, self.angle)
        
        
    def advance(self):
        super().advance()
        self.angle += self.spin
    
    @abstractmethod
    def split(self):
        return NotImplemented
        
    
    def __repr__(self):
        return f'{self.name}: Center:{self.center}, Velocity:{self.velocity}, Angle:{self.angle}'
        
    
    

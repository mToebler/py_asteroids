"""
File: rock.py
Author: Mark Tobler
Description: Rock class captures the idea of a flying rock in a 0 gravity 
environment. Rock extends Flyer class.
"""
import arcade
import random
import constants
from abc import ABC
from point import Point
from velocity import Velocity
from flyer import Flyer
from angularvelocity import AngularVelocity

class Rock(Flyer, ABC):
    """
    Just a medium type like rock in 0 gravity environment.
    """
    
    def __init__(self, startPoint=None, startVelocity=None):
        super().__init__()
        self.name = 'Rock'
        #arcade image        
        self.texture = None #arcade.load_texture(None)
        self.spin = 0
        if startPoint is None:            
            self.center = Point(random.randint(1, constants.SCREEN_WIDTH), random.randint(1, constants.SCREEN_HEIGHT))
        else:
            self.center = startPoint
        self.angle = random.randint(1, 360)
    
    def draw(self):
        """
        used by extending classes to draw using texture
        """
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, self.angle)
        
        
    def advance(self):
        super().advance()
        self.angle += self.spin
        
    
    def __repr__(self):
        return f'{self.name}: center:{self.center}, velocity:{self.velocity}'
        
    
    

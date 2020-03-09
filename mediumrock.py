"""
File: rock.py
Author: Mark Tobler
Description: Rock class captures the idea of a flying rock in a 0 gravity 
environment. Rock extends Flyer class.
"""
import arcade
import random
import constants
from point import Point
from velocity import Velocity
from rock import Rock
from smallrock import SmallRock
from angularvelocity import AngularVelocity

class MediumRock(Rock):
    """
    Just a medium type like rock in 0 gravity environment.
    """
    MEDIUM_ROCK_SPIN = -2
    MEDIUM_ROCK_RADIUS = 5

    def __init__(self, startPoint, startVelocity):
        super().__init__(startPoint, startVelocity)        
        #arcade image
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'meteorGrey_med1.png')
        self.radius = self.texture.width/2
        self.spin = MediumRock.MEDIUM_ROCK_SPIN        
        #self.radius = MediumRock.MEDIUM_ROCK_RADIUS
        # only bigrocks get an initial velocity. Other rocks inherit theirs 
        # from the rock it breaks off from
        # TAKES PLACE IN PARENT ABSTRACT CLASS
        # self.velocity = startVelocity
        
    def split(self):
        """
        If hit, it breaks apart and becomes two small asteroids (1 & 2):
            1. The [1st] small asteroid has the same velocity as the original 
                medium one plus 1.5 pixels/frame up and 1.5 pixels/frame to the right.
            2. The second, 1.5 pixels/frame down and 1.5 to the left.
        """
        if (constants.DEBUG):
            print('MediumRock: split: split!!')
        shards = set()
        rock = SmallRock(self.center, self.velocity)
        # y axis is up.
        rock.velocity.dy += 1.5
        rock.velocity.dx += 1.5
        if (constants.DEBUG): 
            print('MediumRock.split(): 1st rock: ', rock)
        shards.add(rock)
        rock = SmallRock(self.center, self.velocity)
        # y axis is up.
        rock.velocity.dy -= 1.5
        rock.velocity.dx -= 1.5
        if (constants.DEBUG): 
            print('MediumRock.split(): 2st rock: ', rock)
        shards.add(rock)
        
        return shards    
    
    
        
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
from angularvelocity import AngularVelocity

class MediumRock(Rock):
    """
    Just a medium type like rock in 0 gravity environment.
    """
    MEDIUM_ROCK_SPIN = -2
    MEDIUM_ROCK_RADIUS = 5

    def __init__(self, startPoint, startVelocity):
        super().__init__()        
        self.rotation = AngularVelocity(MediumRock.MEDIUM_ROCK_SPIN)
        self.velocity = startVelocity
        #arcade image
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'meteorGrey_med1.png')
        self.radius = self.texture/2
        #self.radius = MediumRock.MEDIUM_ROCK_RADIUS
        # only bigrocks get an initial velocity. Other rocks inherit theirs 
        # from the rock it breaks off from
        self.velocity = startVelocity

        
    
    
        
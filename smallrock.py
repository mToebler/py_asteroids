"""
File: smallrock.py
Author: Mark Tobler
Description: SmallRock brings a set of specifically smaller behaviors and
attributes to the Rock class.
"""
import arcade
from velocity import Velocity
import constants
from rock import Rock

class SmallRock(Rock):
    
    SMALL_ROCK_SPIN = 5
    SMALL_ROCK_RADIUS = 2

    def __init__(self, startPoint, startVelocity):
        super().__init__()
        self.name = 'SmallRock'
        self.center = startPoint
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'meteorGrey_small1.png')
        self.radius = self.texture.width/2
        #TODO FIX! self.radius = BigRock.BIG_ROCK_RADIUS
        self.spin = SmallRock.SMALL_ROCK_SPIN
        # only bigrocks get an initial velocity. Other rocks inherit theirs 
        # from the rock it breaks off from
        self.velocity = startVelocity

        
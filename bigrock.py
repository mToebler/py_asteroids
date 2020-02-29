"""
File: bigrock.py
Author: Mark Tobler
Description: BigRock brings a set of specific behaviors and attributes to 
the Rock class.
"""
import arcade
import constants
from rock import Rock
from point import Point
from velocity import Velocity


class BigRock(Rock):
    """
    A big rock extending rock. I'm trying to think what the value add rock is 
    bringing to the table for the time being.... 8-c
    """
    BIG_ROCK_SPIN = 1
    BIG_ROCK_SPEED = 1.5
    BIG_ROCK_RADIUS = 15

    def __init__(self, startPoint=Point()):
        super().__init__(startPoint)
        self.name = 'BigRock'
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'meteorGrey_big1.png')
        self.radius = self.texture.width/2
        #TODO FIX! self.radius = BigRock.BIG_ROCK_RADIUS
        self.spin = BigRock.BIG_ROCK_SPIN
        
        #only bigrocks get an initial velocity
        self.velocity = Velocity.velocity_from_speed_angle(BigRock.BIG_ROCK_SPEED, self.angle) 
        #everything else should be in Rock
        
        
    
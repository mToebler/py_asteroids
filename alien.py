"""
Author:      Mark Tobler
File:        Alien.py
Description: Flying alien space ship. Alien ship image is provided by 
            FreeIconsPNG.com. This icon has been altered to clear its. 
            background and colored green. The alien people and technology
            are immune from asteroid impacts. They are like shepherds
            to their asteroid flock. /s
            
"""

import arcade 
import random
import constants
import math
from velocity import Velocity
from alienbullet import AlienBullet
from flyer import Flyer
from point import Point
from rock import Rock


class Alien(Rock):
    """
    Alien ship appears randomly only when there are fewer than 5 asteroids
    left on screen. It will appear on either left or right
    edge, and the alien ship flys through to the opposite side taking
    an angular, zig-zag path. It fires limited range bullets at the 
    player ship.
    """
    # plan is to add this directly to the rocks collection in Game...?
    # Some constant properties:
    CHANGE_CHANCE = 80
    #APPEAR_CHANCE = 750
    APPEAR_CHANCE = 250
    #FIRE_CHANCE = 100
    FIRE_CHANCE = 25
    
    def __init__(self):
        super().__init__()        
        if random.random() * 100 % 2 > 1:
            # so center will have an x = 0 and velocity will need to be x +
            self.center = Point(0, random.random() * constants.SCREEN_HEIGHT)
            self.velocity = Velocity(2.0, 2.0)
        else:
            # so center will have an x = SCREEN_WIDTH and velocity will need to be x -
            self.center = Point(constants.SCREEN_WIDTH, random.random() * constants.SCREEN_HEIGHT)
            self.velocity = Velocity(-2.0, 2.0)
        if random.random() * 100 % 2 > 1:
            self.texture = arcade.load_texture(constants.PATH_IMAGES + 'alien_ship_green-sm.png')
        else:
            self.texture = arcade.load_texture(constants.PATH_IMAGES + 'alien_ship_green.png')
        self.radius = self.texture.width//2 * 0.75
        self.angle = 0
        
    def advance(self):
        """
        Moves alien forward. Checks on progress moving across screen.
        Alien changes direction sporadically.
        """
        if random.random() * Alien.CHANGE_CHANCE < 2:
            # change dy polarity
            self.velocity.dy *= -1
        super().advance()
        
    def split(self):
        self.alive = False
        return set()

    def fire(self, target):
        """
        Returns an AlienBullet with a trajectory towards the target's'
        current location.
        """
        angle = math.atan2(target.center.y - self.center.y, target.center.x - self.center.x)
        angle = angle * 180/math.pi  #convert to degrees        
        # put the origin point of the bullet far enough
        # away it does not photon itself.
        radius_adjust = self.texture.height/2 * 1.25
        laser_barrel_end = Point(radius_adjust * Velocity.cosine(angle), 
                                radius_adjust * Velocity.sine(angle))
        laser_barrel_end = laser_barrel_end + self.center
        
        p = Point(laser_barrel_end.x, laser_barrel_end.y)
        v = Velocity(self.velocity.dx, self.velocity.dy)
        
        return AlienBullet(p, angle, v)
    
        
        
        
    
    
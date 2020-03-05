"""
Author: Mark Tobler
File: ship.py
"""
from velocity import Velocity
from limited_velocity import LimitedVelocity
import math
import random
import arcade
import constants
from flyer import Flyer
from angularvelocity import AngularVelocity
from point import Point
from bullet import Bullet

class Ship(Flyer):
    """
    Captures the idea of a flying ship in zero gravity. Ship extends flyer. 
    Uses LimitedVelocity instead of Velocity. Restricting speeds of the 
    ship.
    """
    #class constants
    SHIP_TURN_AMOUNT = 3
    SHIP_RADIUS = 30
    SHIP_THRUST_AMOUNT = 0.25

    def __init__(self):
        super().__init__()
        self.name = 'Ship'
        self.center = Point(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
        self.rotation = AngularVelocity(1)
        # overriding Flyer to use LimitedVelocity
        self.velocity = LimitedVelocity()
        # three textures for emulating flames.
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange.png')
        self.thrusting_texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange_thrust2.png')
        self.thrusting_alt_texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange_thrust2-0.png')
        # self.thrusting_texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange_flames3.png')
        # self.thrusting_alt_texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange_flames2.png')
        self.radius = Ship.SHIP_RADIUS
        # just private
        self.__thrust = Ship.SHIP_THRUST_AMOUNT
        self.__thrusting = False
        
    def turn(self, angle):
        """rotates by the given angle"""
        #AngularVelocity will handle rotations
        self.rotation.angle = self.rotation.angle + angle
        if self.velocity.dx != 0:
            print(f'Ship: turn(): angle = {self.rotation.angle}; radians = {self.rotation.angle *  math.pi / 180}')
        
    def turn_left(self):
        """Turns clockise by Ship.SHIP_TURN_AMOUNT"""
        self.turn(Ship.SHIP_TURN_AMOUNT)
        
    def turn_right(self):
        """Turns counter-clockise by Ship.SHIP_TURN_AMOUNT"""
        self.turn(Ship.SHIP_TURN_AMOUNT * -1)
    
    def thrust(self):
        """Applies force towards the current angle's direction"""
        dx = self.velocity.dx + (self.__thrust * Velocity.cosine(self.rotation.angle + 90))
        dy = self.velocity.dy + (self.__thrust * Velocity.sine(self.rotation.angle + 90))
        # in order to get around limits hindering movement when approaching limit.
        self.velocity.set_velocity(dx, dy)
        # print(f"SHIP: thrust: can't set new velocity values: {dx},{dy}; current: {self.velocity}")

        # self.velocity.dx += self.__thrust * math.cos(math.pi * (self.rotation.angle) / 180.0) 
        # self.velocity.dy += self.__thrust * math.sin(math.pi * (self.rotation.angle) / 180.0)        
        self.__thrusting = True
        
    def fire(self):
        """
        The ship fires the bullet, passing on its own angle and velocity 
        """
        # need to adjust center point to take into account the length or the ship, or barrel
        # of laser cannon. adjacent is going to be the radius for this calculation.
        radius_adjust = self.texture.height - 1
        lazer_barrel_end = Point(radius_adjust * Velocity.cosine(self.rotation.angle + 90), 
                                 radius_adjust * Velocity.sine(self.rotation.angle + 90))
        lazer_barrel_end = lazer_barrel_end + self.center
        return Bullet(lazer_barrel_end, self.rotation.display_angle, self.velocity)

    def advance(self):  
        """Moves Ship from one moment to the next."""
        # with ship, there's velocity as well as rotational veloctiy 
        # that needs to be considered. 
        self.center.move_by(self.velocity)
        # implementing this at a later date
        self.rotation.advance()

    def draw(self):
        """
        used by extending classes to draw using texture
        """
        if (self.__thrusting):
            # testing for a random even based number here
            if random.random() * 10 % 2 < 1:
                arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.thrusting_texture, (self.rotation.angle))
            else:
                # drawing the alt texture to give the appearance of flickering thrust flames
                arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.thrusting_alt_texture, (self.rotation.angle))
            self.__thrusting = False
        else:
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, (self.rotation.angle))
        
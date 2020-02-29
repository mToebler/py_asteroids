"""
Author: Mark Tobler
File: ship.py
"""
import math
import arcade
import constants
from flyer import Flyer
from angularvelocity import AngularVelocity
from point import Point

class Ship(Flyer):
    """
    Captures the idea of a flying ship in zero gravity. Ship extends flyer.
    """
    #class constants
    TURN_SIZE = 3

    def __init__(self):
        super().__init__()
        self.name = 'Ship'
        self.center = Point(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
        self.rotation = AngularVelocity(1)
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange.png')
        self.radius = 30
        # just private
        self.__thrust = 0.25 
        
    def turn(self, angle):
        """rotates by the given angle"""
        #AngularVelocity will handle rotations
        self.rotation.angle = self.rotation.angle + angle
        print(f'Ship: turn(): angle = {self.rotation.angle}')
        
    def turn_left(self):
        """Turns clockise by Ship.TURN_SIZE"""
        self.turn(Ship.TURN_SIZE)
        
    def turn_right(self):
        """Turns counter-clockise by Ship.TURN_SIZE"""
        self.turn(Ship.TURN_SIZE * -1)
    
    def thrust(self):
        """Applies force towards the current angle's direction"""
        self.velocity.dx += self.__thrust * math.cos(math.pi * (self.rotation.angle+90) / 180.0) 
        self.velocity.dy += self.__thrust * math.sin(math.pi * (self.rotation.angle+90) / 180.0)

    def advance(self):
        """Moves Ship from one moment to the next."""
        # with ship, there's velocity as well as rotational veloctiy 
        # that needs to be considered. 
        self.center.move_by(self.velocity)
        # implementing this later
        self.rotation.advance()

    def draw(self):
        """
        used by extending classes to draw using texture
        """
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, (self.rotation.angle))
        
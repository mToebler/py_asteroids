"""
Author: Mark Tobler
File: ship.py
"""
from timerrock import TimerBullet
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
from rock import Rock

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
    SHIELD_LIST = [arcade.color.LAVENDER_MIST, arcade.color.ALICE_BLUE, arcade.color.LIGHT_GRAY, arcade.color.PALE_SILVER, arcade.color.LAVENDER_GRAY]
    
    def __init__(self):
        super().__init__()
        self.center = Point(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
        self.rotation = AngularVelocity(1)
        # overriding Flyer to use LimitedVelocity
        self.velocity = LimitedVelocity()
        # Using a sprite to reduce the size of the ship. Adding two 
        # textures for thrusting effects. 
        self.sprite = arcade.Sprite(constants.PATH_IMAGES + 'playerShip1_orange.png', 0.60)
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange.png')
        self.thrusting_texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange_thrust2.png')
        self.thrusting_alt_texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange_thrust2-0.png')
        self.shielding_texture = arcade.load_texture(constants.PATH_IMAGES + 'playerShip1_orange_shields2.png')
        self.sprite.textures.append(self.thrusting_texture) # this is texture 1
        self.sprite.textures.append(self.thrusting_alt_texture) # this is texture 2
        self.sprite.textures.append(self.shielding_texture) # this is texture 3
        self.sprite.set_texture(0) # the original image
        self.radius = self.sprite.height / 2  * 0.9 #Ship.SHIP_RADIUS
        self.lives = constants.LIVES
        self.shielding = False
        
        #protected
        self._iteration_hits = 0
        
        # just private
        self.__thrust = Ship.SHIP_THRUST_AMOUNT
        self.__thrusting = False

    def turn(self, angle):
        """rotates by the given angle"""
        #AngularVelocity will handle rotations
        self.rotation.angle = self.rotation.angle + angle        
        if (constants.DEBUG): print(f'Ship: turn(): angle = {self.rotation.angle}; radians = {self.rotation.angle *  math.pi / 180}')
        
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
        self.__thrusting = True
        
    def fire(self):
        """
        The ship fires the bullet, passing on its own angle and velocity 
        """
        # need to adjust center point to take into account the length or the ship, or barrel
        # of laser cannon. adjacent is going to be the radius for this calculation.
        if(self.alive):
            radius_adjust = self.texture.height/2 + 2
            lazer_barrel_end = Point(radius_adjust * Velocity.cosine(self.rotation.angle + 90), 
                                    radius_adjust * Velocity.sine(self.rotation.angle + 90))
            lazer_barrel_end = lazer_barrel_end + self.center
            return Bullet(lazer_barrel_end, self.rotation.display_angle, self.velocity)
        else:
            return TimerBullet()
    
    def hit(self, rock=None):
        """
        Registers hits, activates shields, and determines ship's reaction.
        """
        damage = 0
        if self.lives > 0:
            self.shielding = True            
            if (rock is None):
                damage = 1
            elif isinstance(rock, Rock):
                damage = rock.damage
                # velocity changes on impact. Add velocities together
                v = rock.velocity
                if rock.spin != 0 :
                    v.dx *= 1/(abs(rock.spin) * 1.25)
                    v.dy *=  1/(abs(rock.spin) * 1.25)
                    v = self.velocity + v
                    self.velocity.set_velocity(v.dx * 0.65, v.dy * 0.65)
            else :
                damage = 1 # maybe this could be added to initial if
        else:
            self.alive = False
        self.lives -= damage; self.lives = 0 if self.lives < 0 else self.lives
        self._iteration_hits += damage
        
    def advance(self):  
        """Moves Ship from one moment to the next."""
        self.center.move_by(self.velocity)
        # implementing this at a later date
        #self.rotation.advance()
        self.sprite.center_x = self.center.x
        self.sprite.center_y = self.center.y
        self.sprite.angle = self.rotation.angle 

    def draw(self):
        """
        Draws the ship (a sprite) using 1 of 3 textures depending on Game state.
        """
        if (self.alive):
            if (self.__thrusting):
                # drawing the alt texture to give the appearance of flickering 
                # thrust flames
                # testing for a random even-esque number here
                if random.random() * 10 % 2 < 1:
                    self.sprite.set_texture(1)                    
                else:                    
                    self.sprite.set_texture(2)
                    
                self.__thrusting = False
            else:
                self.sprite.set_texture(0)
            self.sprite.draw()
            if (self.shielding or self._iteration_hits > 0):
                self.sprite.set_texture(3)
                self.sprite.draw()
                arcade.draw_ellipse_outline(self.center.x, self.center.y, 
                            (self.sprite.width * 1.15), 
                            (self.sprite.height * 1.15), 
                            color=Ship.SHIELD_LIST[self._iteration_hits%len(Ship.SHIELD_LIST)], 
                            tilt_angle=self.rotation.angle)
                if(constants.DEBUG):
                    print(f'ship.draw.shielding: iteration_hits: {self._iteration_hits} color: {Ship.SHIELD_LIST[self._iteration_hits%len(Ship.SHIELD_LIST)]}')
                self.shielding = False; self._iteration_hits -= 1
                
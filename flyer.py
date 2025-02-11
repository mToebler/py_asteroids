"""
Author: Mark Tobler
File: flyer.py
"""
import arcade 
from abc import ABC, abstractmethod
import constants
from point import Point
from velocity import Velocity

class Flyer(ABC):
    """
    Description: This is the base class for objects that fly, or move through
    a cartesian plane by means of an applied Velocity. The Flyer class is 
    not meant to be instanciated per se, and is marked as an ABC (abstract 
    base class). It provides the following framework for the extending 
    classes:
    Properties:
        center : Point representing the geometric center of the object.
        velocity : the vector equivalent of speed. has both distance 
                over time and direction.
        radius : float - the distance from object's center to its boundary   
                if another object crosses this boundary, collision!
        alive : boolean - so, is_alive, indicating its viability. will
                indicate if it is rendered or not (by draw()) and removed
    Methods:
        advance() : None - processes state from frame to frame. logic.
        draw() : None - how an object represents on the screen. like a 
                    __repr__(), but graphical.
        is_off_screen(int screen_width, int screen_height) : boolean - 
                a bit out of a flyer's awareness, perhaps, but is aware
                of crossing a given boundary and reporting back. 
                think 'check_beyond_point(x,y)'
        
"""
    # marked as abstract base class
    def __init__(self):
        # while Flyer should be considered abstract, this lays out
        # the framework here. See notes above.
        self.name = self.__class__.__name__
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 1
        self.alive = True
        # all flyers have a color. Here to back up any that don't specify
        self.color = arcade.color.PINK
        self.angle = 0
        # loading an empty image for this. Re-evaluate if performance hit.
        self.texture = None # arcade.load_texture(constants.PATH_IMAGES + 'stub.png')
        
    def advance(self):
        """Override if more complex than simple move by velocity"""
        self.center.move_by(self.velocity)

    def draw(self):
        """
        Implementing classes should override this draw method unless 
        they are more than a texture being drawn on screen.
        See Flyer notes above.
        """
        # likely will be overridden to appropriate shapes
        # Bullet and target use this as is. Not making abstractmethod.
        if self.alive:
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, self.angle)

    def is_off_screen(self, screen_width, screen_height):
        # check if either x or y is past the provided coordinates.
        # creating a point out of provided coordinates and comparing
        # it to center as Point has rich comparators implemented
        limit = Point(screen_width, screen_height)
        return (self.center - self.radius) > limit
    
    def is_near(self, otherFlyer):
        """
        Using point's subtractive comparison ability, checking if other
        flyer and this instance are is within each other's radii
        """
        # subtracting the greater's one center point from the other and 
        # returning true if that point falls within range of the square of the 
        # combined radii.
        #if ((self.center * self.center) > (otherFlyer.center * otherFlyer.center)):
        distance = self.center - otherFlyer.center
        return_value = False
        if abs(distance.x) <= self.radius + otherFlyer.radius and abs(distance.y) <= self.radius + otherFlyer.radius:
            if (constants.DEBUG):
                print(f'DEBUG: flyer.is_near: returning TRUE for is_near: distance is {distance}')
            return_value = True
        return return_value
        
    def __repr__(self):
        return f'{self.name}: c:{self.center} r:{self.radius} v:{self.velocity}'    
    

"""
Author: Mark Tobler
File: bullet.py
"""
import math
import constants
import arcade
from velocity import Velocity
from flyer import Flyer

class Bullet(Flyer):
    """
    Encapsulates the idea of an arcade game-type bullet. A bullet
    is created when another object fires it. When initialized, 
    a bullet will add it's own velocity to that which it has inherited.
    """    
    BULLET_RADIUS = 2  # 30 seems TOO high!
    BULLET_SPEED = 10
    BULLET_LIFE = 30

    def __init__(self, start_point, angle, inherited_velocity):
        # adds Bullet_speed to this velocity
        super().__init__()
        self._damage = 1
        self.angle = angle
        self.life = Bullet.BULLET_LIFE
        # this velocity assignment is taken from the instructions in the 
        # assignment:
        #   "Bullets are should [sic] start with the same velocity of the ship 
        #    (speed and direction) plus 10 pixels per frame in the direction 
        #    the ship is pointed." 
        # Let me know if this is not what you want. It makes sense logically, 
        # but in cases where the ship is going faster than bulllet speed, the 
        # bullet appears to have a negative direction.#
        self.velocity = inherited_velocity + Velocity.velocity_from_speed_angle(Bullet.BULLET_SPEED, self.angle)
        # old calculation below.
        #self.velocity = Velocity.velocity_from_speed_angle(inherited_velocity.speed + Bullet.BULLET_SPEED, (self.angle)) 
        
        # bullet center should be the ship's center plus the length of the ship's radius in the 
        # proper direction. Taken care of in ship. Bullet is ignorant of ship.
        self.center = start_point
        # originally this was not a texture asset. it was just a small dot bullet.
        # having implemented this after implementing the other texture assets (rocks & ship)
        # I realize that texture should have been made a part of flyer. For this milestone
        # anyhow, it will remain individual extended class attributes rather than inherited.
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'laserBlue01.png')
        self.radius = Bullet.BULLET_RADIUS
        
        #by taking the velocity.dx dividing it by the cos if the angle in radians should give the speed
        #to which add 10, then recalculate the dx, dy of velocity.
        
    @property
    def damage(self):
        return self._damage
    
    # no setter for damage. This is protected 
    
    def draw(self):
        """Only draws itself 60 times"""
        #super().draw()
        super().draw() #arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, (self.angle))
        #self.life -= 1    #TODO: put this in advance() ??? 
        
    def advance(self):
        super().advance()
        self.life -= 1
        if self.life < 1:
            self.alive = False
            
        

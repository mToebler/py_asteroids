"""
Author: Mark Tobler
File: bullet.py
"""
import math
from velocity import Velocity
from flyer import Flyer

class Bullet(Flyer):
    """
    Encapsulates the idea of an arcade game-type bullet. A bullet
    is created when another object fires it. When initialized, 
    a bullet will add it's own velocity to that which it has inherited.
    """    
    BULLET_RADIUS = 30
    BULLET_SPEED = 10
    BULLET_LIFE = 60

    def __init__(self, start_point, angle, inherited_velocity):
        # adds Bullet_speed to this velocity
        super().__init__()
        self._damage = 1
        self.center = start_point
        self.angle = angle
        self.life = Bullet.BULLET_LIFE
        self.velocity = Velocity.velocity_from_speed_angle(inherited_velocity.speed + Bullet.BULLET_SPEED, (self.angle)) 
        #by taking the velocity.dx dividing it by the cos if the angle in radians should give the speed
        #to which add 10, then recalculate the dx, dy of velocity.
        
    @property
    def damage(self):
        return self._damage
    
    # no setter for damage. This is protected 
    
    def draw(self):
        """Only draws itself 60 times"""
        super().draw()
        self.life -= 1    
        
    def advance(self):
        super().advance()
        self.life -= 1
        if self.life < 1:
            self.alive = False
            
        
        
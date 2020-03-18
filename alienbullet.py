"""
Author:Mark Tobler
File: alienbullet.py
Description: AlienBullet extends noth the Bullet class and the Rock class. It
            is using the Rock class more as an interface so that it can
            be put into the rocks collection in Game to allow for 
            collision checks. As such, it implements the abstract split method.
            
            Alien laser sprite is provided for free from PNGImage.net.
            title="laser sprite png" 
            href="https://pngimage.net/laser-sprite-png/"
"""
import arcade
from bullet import Bullet
from rock import Rock
import constants

class AlienBullet(Bullet, Rock):
    BULLET_LIFE = 20
    
    def __init__(self, start_point, angle, inherited_velocity):
        #expecting angle to be figured out to be the sin (or cos) 
        # of a line from Alien's center to the player's ship's center
        # this will happen in game
        super().__init__(start_point, angle, inherited_velocity)
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'alien_laser2-0.png')
        self.radius = self.texture.width//2 * 0.75
        self.life = AlienBullet.BULLET_LIFE
        self._damage = 5
        
    def split(self):
        """
        Returns an empty set. May return an explosion
        """
        return set()
    
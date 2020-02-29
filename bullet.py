"""
Author: Mark Tobler
File: bullet.py
"""
from flyer import Flyer

class Bullet(Flyer):
    """
    Encapsulates the idea of an arcade game-type bullet.
    """
    def __init__(self):
        super().__init__()
        self._damage = 1
        
    @property
    def damage(self):
        return self._damage
    
    # no setter for damage. This is a protected 
    
    def fire(self):
        """Perhaps this belongs in ship."""
        pass
        
        
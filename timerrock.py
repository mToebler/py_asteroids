"""
File: timerrock.py
Author: Mark Tobler
Description: An invisible, formless rock which exists for x number
of frames to allow time to pass without jumpy transitions.
"""
import arcade
from velocity import Velocity
import constants
from point import Point
from rock import Rock

class TimerRock(Rock):
    
    TIMER_ROCK_DEFAULT_FRAMES = 90

    def __init__(self, frames=TIMER_ROCK_DEFAULT_FRAMES):
        super().__init__(Point(), Velocity())
        self.texture = None
        self.radius = 0
        self.spin = 0
        self.frames = frames
        
    def split(self):
        if (constants.DEBUG):
            print('\nTimer rocks return empty set.\n')
        return set()
    
    def advance(self):
        self.frames -= 1
        if self.frames < 1:
            self.alive = False
    
    def draw(self):
        pass    
    
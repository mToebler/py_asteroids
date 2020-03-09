"""
File: bigrock.py
Author: Mark Tobler
Description: BigRock brings a set of specific behaviors and attributes to 
the Rock class.
"""
from smallrock import SmallRock
from mediumrock import MediumRock
import arcade
import constants
from rock import Rock
from point import Point
from velocity import Velocity


class BigRock(Rock):
    """
    A big rock extending (abstract) rock.
    """
    BIG_ROCK_SPIN = 1
    BIG_ROCK_SPEED = 1.5
    BIG_ROCK_RADIUS = 15

    def __init__(self, startPoint=Point()):
        super().__init__(startPoint)
        self.texture = arcade.load_texture(constants.PATH_IMAGES + 'meteorGrey_big1.png')
        self.radius = self.texture.width/2
        #TODO FIX! self.radius = BigRock.BIG_ROCK_RADIUS
        self.spin = BigRock.BIG_ROCK_SPIN
        
        #only bigrocks get an initial velocity
        self.velocity = Velocity.velocity_from_speed_angle(BigRock.BIG_ROCK_SPEED, self.angle) 
        #everything else should be in Rock
        
        
    def split(self):
        """
        If a large asteroid gets hit, it breaks apart and becomes 
        two medium asteroids (1,2) and one small one (3): 
            1. The first medium asteroid has the same velocity as the 
                original large one plus 2 pixel/frame in the up direction.
            2. The second medium asteroid has the same velocity as the 
                original large one plus 2 pixel/frame in the down direction.
            3. The small asteroid has the original velocity plus 
                5 pixels/frame to the right.
        """
        # This method will return a collection of these objects.
        # Why are these here and not in the game class? Consider moving.
        # Does having it here better fit the python ethos of having the
        # objects take care of object matters? Does this break the object
        # model? Objects in RL split or break all the time; in their 
        # deaths rise up other objects; this happens at the object level,
        # like die() or fire() or hit(). Also taking care of it at the 
        # object level let's us take whatever they send back and stick 
        # it in the rocks collection all in one swoop.
        if (constants.DEBUG):
            print(f'\n\nBigRock: split: split!!')
        # create the return collection.
        shards = set()
        rock = MediumRock(self.center, self.velocity)
        # y axis is up.
        rock.velocity.dy += 2
        if( constants.DEBUG): 
            print('BigRock.split(): 1st rock: ', rock)
        shards.add(rock)
        # 2nd med. rock:
        rock = MediumRock(self.center, self.velocity)
        # y axis is up.
        rock.velocity.dy -= 2
        if( constants.DEBUG): 
            print('BigRock.split(): 2nd rock: ', rock)
        shards.add(rock)
        
        rock = SmallRock(self.center, self.velocity)
        rock.velocity.dx += 5
        if( constants.DEBUG): 
            print('BigRock.split(): 3rd rock: ', rock)
        shards.add(rock)
        
        return shards
        
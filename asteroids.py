"""
File: asteroids.py
Original Author: Br. Burton
Student Author: Mark Tobler
Designed to be completed by others
This program implements an asteroids game.
"""
from math import e
from os import system
import time
import random
import arcade
import constants
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from point import Point
# from velocity import Velocity
from ship import Ship
#from rock import Rock
from bigrock import BigRock
from smallrock import SmallRock


# These are Global constants to use throughout the game
# These have been moved to constants or to each applicable class
# so they can be accessed like so: Bullet.BULLET_RADIUS

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.reset = True
        self.held_keys = set()
        
        self.ship = Ship()
        # TODO: Consider turning these into python sets rather than lists.
        #       Removing elements from the middle would be faster.
        self.rocks = []
        # need to setup the rocks.
        self.bullets = []
        self.score = 0    
        # game should keep track of lives, not ship, IMO.
        # lives it outside of ship's scope.
        # TODO: declare anything here you need the game class to track

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        for rock in self.rocks:
#            print(f'Asteroids: on_draw: drawing {rock}')
            rock.draw()
            
        for bullet in self.bullets:
            bullet.draw()
            
        self.ship.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        if (self.reset):
            self.reset = False
            random.seed()
            #generate rocks
            for r in range(constants.INITIAL_ROCK_COUNT):
                point = Point((random.random() * constants.SCREEN_WIDTH), 
                            (random.random() * constants.SCREEN_HEIGHT))
                self.rocks.append(BigRock(point))
            self.ship = Ship()
            time.sleep(2)        
        
        if len(self.rocks) < 1:
            self.reset = True
            self.bullets.clear()
            if(constants.DEBUG): print('Game: Resetting!')
            #!!! increase starting rock count
            constants.INITIAL_ROCK_COUNT += 1

        self.check_keys()
        self._advance_flyers(self.rocks)
        self._advance_flyers(self.bullets)
        self.ship.advance()
        self._check_boundaries()
        self._check_zombies()
        
        # TODO: Tell everything to advance or move forward one step in time

        # TODO: Check for collisions
        self._check_flyer_collisions()

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.turn_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.turn_right()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust()

        if arcade.key.DOWN in self.held_keys:
            pass

        # Machine gun mode...
        if arcade.key.SPACE in self.held_keys:
            self.bullets.append(self.ship.fire())


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                self.bullets.append(self.ship.fire())

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
            
    def _advance_flyers(self, flyers):
        for flyer in flyers:
#            print(f'Asteroid: advancing flyer {flyer}')
            flyer.advance()
            
    def _check_flyer_collisions(self):
        """ check for collisions amongst the rocks for bullets, and ship"""
        # create a temp collection to hold the created rocks during this process.
        new_rocks = set()
        # hmmm... is there anyother way than to iterate through the lists
        # and compare one at a time?
        for rock in self.rocks:
            # these both have flyer's center points which has +, - and 
            # comparison ability
            for bullet in self.bullets:
                temp_rocks = None
                if (rock.is_near(bullet)):                    
                    if (constants.DEBUG): 
                        print(f'debug: game._check_flyer_collisions: {bullet}')
                    temp_rocks = rock.split() 
                    for tr in temp_rocks:
                        new_rocks.add(tr)
                        if (constants.DEBUG): 
                            print(f'\n\ndebug: game._check_flyer_collisions: added {tr} to\nnew_rocks:{new_rocks}')
                                            
                    rock.alive = False
                    bullet.alive = False
                    continue
                    # on to the next bullet. Both rock/bullet will be removed
                    # during zombie check.
            
            if rock.is_near(self.ship):
                if (constants.DEBUG):
                    print(f'debug: game._check_flyer_collisions: {self.ship}')
                    print(f'debug: game._check_flyer_collisions: {rock}')
                #self.ship.alive = False
        # now add new_rocks set to the mix:
        if len(new_rocks) > 0 : 
            for r in new_rocks: # when self.rocks becomes a set, this will change. TODO
                self.rocks.append(r)
            
    def _check_boundaries(self):
        """
        Checks for and adjusts flyers center if affected by screen limits
        """
        edgePoint = Point(SCREEN_WIDTH,SCREEN_HEIGHT)
        # the ship
        self._wrap_flyer(self.ship)
        #TODO: the radius doesn't seem right. FIX
        # the rocks
        for flyer in self.rocks:
            # if flyer.center- flyer.radius > edgePoint:
            #     self._wrap_flyer(flyer)
            # elif flyer.center+ flyer.radius < Point():
            self._wrap_flyer(flyer)
        # the bullets
        for flyer in self.bullets:
            self._wrap_flyer(flyer)
    
    def _check_zombies(self):
        for flyer in self.rocks:
            if not flyer.alive:
                self.rocks.remove(flyer)
        
        for flyer in self.bullets:
            if not flyer.alive:
                self.bullets.remove(flyer)
                
    
    def _wrap_flyer(self, flyer):
        """
        manipulates a flyer's center point to wrap around the arcade window
        """
        # should the game wrap the flyer or should the flyer wrap the flyer?
        # I believe it is within game's scope.
        # The flyer is here because one of it's center vector values is 
        # crossing over. Two options:
        #   1. Simply 0 or MAX out the flyer.vector value in question.
        #   2. Create another flyer with the same attribute values
        #      and add it to the flyer collection. This will allow 
        #      it to appear that the flyer is actually warping the screen, 
        #      while the original is silently removed after completely 
        #      crossing a boundary. This would complicate collisions, scoring.
        #   BONUS OPTION: Kick it over to flyer.draw to handle the visual 
        #      wrapping, this method will only adjust a center if the flyer
        #      has truly crossed the halfway point.
        if flyer.center.x - flyer.radius > SCREEN_WIDTH:
            flyer.center.x -= SCREEN_WIDTH + 2*flyer.radius
        elif flyer.center.x + flyer.radius < 0:
            flyer.center.x += SCREEN_WIDTH + 2*flyer.radius
            # now for y:
        if flyer.center.y - flyer.radius > SCREEN_HEIGHT:
            flyer.center.y -= SCREEN_HEIGHT + 2*flyer.radius
        elif flyer.center.y + flyer.radius < 0:
            flyer.center.y += SCREEN_HEIGHT + 2*flyer.radius

            
            
        
        
# Creates the game and starts it going
window = Game(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
arcade.run()
"""
File: asteroids.py
Original Author: Br. Burton
Student Author: Mark Tobler
Designed to be completed by others
This program implements an asteroids game.
"""
from velocity import Velocity
from alienbullet import AlienBullet
import math
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
from alien import Alien
from timerrock import TimerRock
from limited_velocity import LimitedVelocity


# These are Global constants to use throughout the game
# These have been moved to constants or to each applicable class
# so they can be accessed like so: Bullet.BULLET_RADIUS

# TODO: 
# 1. Scoring. Implement a scoring structure.
#       Score will display with a mid range alpha value
#       Big rock:    5 pts
#       Med rock:   10 pts
#       Sm rock:    15 pts
#       Alien ship: 25 pts
#       Alien lzr:   0 pts
#       Perhaps every 100 pts an extra y seconds of shields awarded.#
# 2. Shielding for ship. 
#       ship starts with x number of seconds of shields.
#       when a level is cleared y seconds is added on top 
#       of remaining shield time. Shield time is automatically
#       deducted depending on the target hit:
#           Big rock = y * .5 seconds
#           Med rock = y * .25 secs
#           Sml rock = y * .125 secs
#           Alien lzr: y * .5 secs
#           Alien shp: y * 1 sec 
#       Shields will simply be a thin circle around the ship. It's 
#       color will change depending on amount of time left and blink
#       when time added:
#           light blue:  > x secs
#           medium blue: < x secs
#           dark blue:   < y secs #  
# or...
# 3. Invincible mode? 
# 4. Better level transitions. Consider having the ship no freeze up.  #
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """
    SCORE_COLOR = arcade.color.ANTI_FLASH_WHITE
    COLOR_LIST_LIGHT = [arcade.color.LAVENDER_MIST, arcade.color.ALICE_BLUE, arcade.color.LIGHT_GRAY, arcade.color.PALE_SILVER, arcade.color.LAVENDER_GRAY]
    COLOR_LIST = [arcade.color.ELECTRIC_LIME, arcade.color.ELECTRIC_YELLOW, arcade.color.ELECTRIC_CRIMSON, arcade.color.ELECTRIC_LAVENDER, arcade.color.ELECTRIC_CYAN]

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLACK) # smokey black is too flat for space.
        self.reset = True
        self.held_keys = set()
        self.respawn_timer = None# 3 state logic here. timer if the ship respawns 
        self.levelup_timer = 90  # time between levels
        self.level = 1
        self.update_rate = 45    # handles speed of game.
        
        self.ship = Ship()
        # using sets not lists
        self.rocks = set()
        # need to setup the rocks.
        self.bullets = {}
        self.bullet_regulator = 1
        self.score = 0    


    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()

        for rock in self.rocks:
#            print(f'Asteroids: on_draw: drawing {rock}')
            rock.draw()
            
        for bullet in self.bullets:
            bullet.draw()
            
        self.ship.draw()
        if not self.ship.alive:
            self.draw_level_status()
        self.draw_info()

    def draw_info(self):
        """
        Puts the current score on the screen.
        Based on Br. Burton's method in Skeet.
        """
        score_text = f"Score: {self.score}\nShields: {self.ship.lives}"
        start_x = 10
        start_y = constants.SCREEN_HEIGHT - 40        
        if self.ship is not None and self.ship.lives / constants.LIVES < 0.5:
            info_color = Game.COLOR_LIST[1]
            if self.ship.lives / constants.LIVES < 0.25:
                info_color = Game.COLOR_LIST[2]
        else:
            info_color = Game.SCORE_COLOR
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, 
                    font_size=12, color=info_color)
        if self.levelup_timer > 0:
            self.levelup_timer -= 1            
            self.draw_level_status(text=f'Level\n{self.level}', use_light=False)
            
    def draw_level_status(self, text='Game\nOver', use_light=True):
        if(use_light): colors = Game.COLOR_LIST_LIGHT
        else: colors = Game.COLOR_LIST
        start_x = constants.SCREEN_WIDTH/2 - 40
        start_y = constants.SCREEN_HEIGHT * 3 / 5
        color = int(constants.HEAP % len(colors))
        color_2 = int(constants.HEAP * 7 % len(colors))
        arcade.draw_text(text, start_x=start_x, start_y=start_y, 
                    font_size=20, color=colors[color], align='center')
        arcade.draw_rectangle_outline(start_x + 32, start_y + 28, 100, 60, colors[color_2])
        constants.HEAP += .05
        
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        if (self.reset and len(self.rocks) < 1 and self.levelup_timer < 1):
            self.set_reset()
            
        if (not self.reset):
            self.process_extras()

        self.check_keys()
        self._advance_flyers(self.rocks)
        self._advance_flyers(self.bullets)
        self.ship.advance()
        self._check_window_boundaries()
        self._check_zombies()
        self._check_flyer_collisions()

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if (self.ship.alive):
            if arcade.key.LEFT in self.held_keys:
                self.ship.turn_left()

            if arcade.key.RIGHT in self.held_keys:
                self.ship.turn_right()

            if arcade.key.UP in self.held_keys:
                self.ship.thrust()

            if arcade.key.DOWN in self.held_keys:
                # warp?
                pass

            # Machine gun mode... TODO: come up with a reasonable machine gun
            #                           implementation.
            if arcade.key.SPACE in self.held_keys :
                if self.bullet_regulator > 0:
                    self.bullets.add(self.ship.fire())
                self.bullet_regulator *= -1
                
    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            #if key == arcade.key.SPACE and arcade.key.SPACE not in self.held_keys:
            #self.bullets.add(self.ship.fire())

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
                            
     #######
    # Special events happen here: i.e., respawning, aliens appearing, 
    # level up...
    ######           
    def process_extras(self):
        """Handles the extras. Separate method keeps update() clean. """
        if len(self.rocks) < 1:
            self.reset = True
            self.level += 1
            self.bullets.clear()
            if(constants.DEBUG): print('Game: Resetting! Adding TimerRock')
            #!!! increase starting rock count
            constants.INITIAL_ROCK_COUNT += 1
            # OR
            self.update_rate += 10
            self.set_update_rate(float(1/self.update_rate))
            self.rocks.add(TimerRock())
            self.levelup_timer = 90
        elif (0 < len(self.rocks) < 3):
            if random.random() * Alien.APPEAR_CHANCE < 1:
                if(constants.DEBUG): print('\n\nUPDATE: !!! Alien  !!!\n\n')
                self.rocks.add(Alien())
        elif (not self.ship.alive):
            # consider putting most if not all of this functionality
            # within SHIP. It would make more sense.
            if self.respawn_timer is None:
                if self.ship.lives > 0:
                    self.ship.lives -= 1
                    self.held_keys.clear()
                    self.ship.velocity = LimitedVelocity()
                    self.ship.center = Point(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
                    self.respawn_timer = 90
            else:
                if self.respawn_timer > 0:
                    self.respawn_timer -= 1
                else:
                    respawn_flag = True
                    for rock in self.rocks:
                        if(self.ship.is_near(rock)):
                            respawn_flag = False
                            self.respawn_timer = 15
                            break
                    if(respawn_flag):
                        self.ship.alive = True
                        self.respawn_timer = None
                        
    def set_reset(self):
        """Sets up asteroid rocks and ship, separate method keeps update() clean."""
        self.reset = False
        random.seed()
        #generate rocks 
        for r in range(constants.INITIAL_ROCK_COUNT):
            if self.ship is not None:
                rerock = True            
                while (rerock):
                    point = Point((random.random() * constants.SCREEN_WIDTH), 
                            (random.random() * constants.SCREEN_HEIGHT))
                    rock = BigRock(point)
                    if not rock.is_near(self.ship):
                        rerock = False
            self.rocks.add(rock)
        if self.ship is None:
            self.ship = Ship()           
        
    def _advance_flyers(self, flyers):
        for flyer in flyers:
#            print(f'Asteroid: advancing flyer {flyer}')
            flyer.advance()
            
    def _check_flyer_collisions(self):
        """ check for collisions amongst the rocks for bullets, and ship"""
        # create a temp collection to hold the created rocks during this process.
        new_rocks = set()
        for rock in self.rocks:
            for bullet in self.bullets:
                temp_rocks = None
                if (rock.is_near(bullet)):
                    self.score += rock.points
                    if (constants.DEBUG): 
                        print(f'debug: game._check_flyer_collisions: {bullet}')
                    temp_rocks = rock.split() 
                    # if(rock.alive):
                    #     self.score += rock.points                    
                    for tr in temp_rocks:
                        new_rocks.add(tr)
                        if (constants.DEBUG): 
                            print(f'\n\ndebug: game._check_flyer_collisions: added {tr} to\nnew_rocks:{new_rocks}')
                    rock.alive = False
                    bullet.alive = False
                    #Both rock/bullet will be removed
                    # during zombie check.                    
                    break;  #break
                    # why break and not continue? break stops all bullets for this dead rock
                    # continue just stops this 
                    # iteration.
                    
            if self.ship.alive and rock.is_near(self.ship):
                if (constants.DEBUG):
                    print(f'\n\ndebug: game._check_flyer_collisions: SHIP HAS BEEN HIT {self.ship}\n\n')
                    print(f'debug: game._check_flyer_collisions: {rock}')
                # this will invoke shields if appropriate
                self.ship.hit(rock) #self.ship.alive = False
                temp_rocks = rock.split()                 
                self.score += rock.points
                for tr in temp_rocks:
                    new_rocks.add(tr)
                rock.alive = False        
                break;
            if isinstance(rock, Alien):
                # chance to fire a bullet at the ship
                if random.random() * Alien.FIRE_CHANCE < 1:
                    # as there is no rock.fire(), going to add this funcitonality here.
                    try:
                        # alien ships shoot only from the "top" quadrant of their ships.
                        angle = math.sin((rock.center.x - self.ship.center.x)/math.sqrt((rock.center.x - self.ship.center.x)**2 + (rock.center.y - self.ship.center.y)**2))
                        angle = angle * 180/math.pi
                    except ZeroDivisionError as e:
                        # going to swallow this e, and move on.
                        print(f'\n\nGame.update: caught a {e}. No biggy, moving on.\n\n')
                        angle = 0
                    finally:
                        # let's add 90 degrees to this angle
                        if(constants.DEBUG): print('_check_flyer_col: angle was ', angle)
                        angle = (angle + 90) % 360
                        # move on . org
                    if(constants.DEBUG): print('_check_flyer_col: now using', angle, ' as angle for alien bullet.')
                    p = Point(rock.center.x, rock.center.y)
                    v = Velocity(rock.velocity.dx, rock.velocity.dy)
                    aBullet = AlienBullet(p, angle, v)
                    if(constants.DEBUG): print('_check_flyer_col: new alien bullet:', aBullet)
                    new_rocks.add(aBullet)
        # now add new_rocks set to the mix:
        if len(new_rocks) > 0 : 
            self.rocks.update(new_rocks)
            
    def _check_window_boundaries(self):
        """
        Checks for and adjusts flyers center if affected by window limits
        """
        #edgePoint = Point(SCREEN_WIDTH,SCREEN_HEIGHT)
        # the ship
        self._wrap_flyer(self.ship)
        # the rocks
        for flyer in self.rocks:
            self._wrap_flyer(flyer)
        # the bullets
        for flyer in self.bullets:
            self._wrap_flyer(flyer)
    
    def _check_zombies(self):
        # Tried two different approaches. Switching out the sets 
        # seemed faster than removing the elements.
        # 1. Switching out the set
        #new_rocks = set()
        # tying set comprehension here
        self.rocks = {rock for rock in self.rocks if rock.alive}
        # for flyer in self.rocks:
        #     if flyer.alive:
        #         new_rocks.add(flyer)
        #         #self.rocks.discard(flyer)
        # self.rocks = new_rocks
        # {rock for rock in self.rocks if rock.alive}
        # # 2, Removing an element from the set.
        self.bullets = {bullet for bullet in self.bullets if bullet.alive}
        # try:
            
        #     for flyer in self.bullets:
        #         if not flyer.alive:
        #             self.bullets.remove(flyer)
        # except KeyError as e:
        #     print('Game._check_zombies: caught KeyError removing a bullet. Moving on.', e)
        
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
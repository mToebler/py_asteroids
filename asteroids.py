"""
File: asteroids.py
Original Author: Br. Burton
Student Author: Mark Tobler
Designed to be completed by others
This program implements an asteroids game.
"""
from random import Random
from velocity import Velocity
from alienbullet import AlienBullet
import math
import random
import arcade
import constants
from point import Point
from ship import Ship
from bigrock import BigRock
from alien import Alien
from timerrock import TimerRock

###
"""
Above and beyonds:
1.: Limited Velocity class put a speed limit in place without hampering 
    ships inertia. Inertia dampens with the down key.
2.: The Ship has shields. Impacts with different sized objects have 
    proportional ship and shield responses: larger objects deduct more 
    from shields; and commensurate velocity is transferred.
3.: Hostile photon shooting Aliens appear by chance when the asteroid 
    count gets below 4. (They've improved their aim at the cost of 
    their range.)
4.: Notable Animations:
      - Ship thrusting & turn impulse flames (thrust flames flicker)
      - Shields activate on impact
      - Background turns every so slightly.
5.: Spin Velocity: similar to the asteroids' spin inertia, the ship 
    utilizes a rotational velocity class though with some dampened inertia
    for playability. Inertia dampens with the down key.
    (The higher the rotational speed, the more it is initially dampened.
     Rotational inertia persists lingeringly by design. Thrusting forward
     mitigates this, or brakes (down), though thrust turning does not.)
6.: Score is kept during the game instance and reacts to remaining shields.
7.: Game can be started when Game Over'ed by hitting RETURN or 'S', 
    'Q' will quit the game between instances. Instructional text appears
    on screen.
8.: Levels: When asteroids & aliens are cleared, the next level starts
    smoothly with an additional asteroid and a slightly faster pace.
9.: Lots of little things if you take the time to examine the code: 
    List comprehensions, multiple inheritance, exception handling, and 
    separation of concerns (mostly). I've tried to apply a consistent 
    object model throughout the game; however these last few weeks have 
    been chaotic (like everyone) and not all the code is cleaned, nor 
    are all the many, many comments sync'd.

As an aside, you suggested perhaps I reduce the comments in my code; 
this was a surprise as most instructors encourage them. My advisor 
continues to support them, citing a marked lack of needed comments within 
the industry and students in particular. Perhaps you could be clearer: 
Comment Quantity? My tone? Consistency? Comments are part of my design 
process. I'd like them to be useful to others, rather than a burden to 
sift through (or worse). Please, truly, more feedback is appreciated. 
I understand you've a larger number of students this semester; I've 
tried to help out where I could.
"""
# Global constants moved to constants.py
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """
    SCORE_COLOR = arcade.color.ANTI_FLASH_WHITE
    COLOR_LIST_LIGHT = [arcade.color.LAVENDER_MIST, arcade.color.ALICE_BLUE, arcade.color.LIGHT_GRAY, arcade.color.PALE_SILVER, arcade.color.LAVENDER_GRAY]
    COLOR_LIST = [(214,176, 98), arcade.color.APPLE_GREEN, arcade.color.ALICE_BLUE, arcade.color.BRANDEIS_BLUE, arcade.color.ELECTRIC_CRIMSON]
    UPDATE_RATE = 50
    START_KEYS = {arcade.key.RETURN, arcade.key.S, arcade.key.R}
    GAME_OVER_KEYS = START_KEYS.union({arcade.key.Q})
    #FONTS = ('Courier New', 'monospace')
    FONTS = ('Lucida Console', 'Monaco', 'monospace')
    
    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLACK) # smoky black is too flat for space.
        self.background = arcade.load_texture(constants.PATH_IMAGES + 'space.png')
        random.seed()
        self.restart()

        
    def restart(self):
        """ Re-starts the Game """        
        self.reset = True
        self.held_keys = set()
        self.respawn_timer = None# 3 state logic here. timer if the ship respawns 
        self.levelup_timer = 90  # time between levels
        self.level = 1
        self.ship = Ship()
        # self.rocks = set()
        self.rocks = []
        self.rock_count = constants.INITIAL_ROCK_COUNT
        # self.bullets = set()
        self.bullets = []
        self.bullet_regulator = 1
        self.score = 0  
        self._text_color_control = 0.0  
        self.update_rate = Game.UPDATE_RATE    # handles speed of game.
        self.set_update_rate(float(1/self.update_rate))        
        motion_polarity = 1 if random.random() * 10 % 2 < 1 else -1
        self.background_angle = 0.0
        self._background_angle_control = 0.002 * motion_polarity
        


    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()
        scale = constants.SCREEN_WIDTH / self.background.width
        arcade.draw_lrwh_rectangle_textured(0, 0,
                        constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT,
                        self.background, angle=self.background_angle)

        for rock in self.rocks:
#            print(f'Asteroids: on_draw: drawing {rock}')
            rock.draw()
            
        for bullet in self.bullets:
            bullet.draw()
            
        self.ship.draw()
        if not self.ship.alive:
            self.draw_level_status()
            self.draw_help_info(text=None, use_light=False)            
        self.draw_info()


    def draw_info(self):
        """
        Puts the current score on the screen.
        Based on Br. Burton's method in Skeet.
        """
        score_text = f"Score: {self.score:5}\nShields: {self.ship.lives:3}"
        start_x = 10
        start_y = constants.SCREEN_HEIGHT - 40        
        
        if self.ship is not None: # and self.ship.lives / constants.LIVES < 0.5:
            color_index = (self.ship.lives-1) * 3 // constants.LIVES 
            info_color = Game.COLOR_LIST[color_index]
        else:
            info_color = Game.SCORE_COLOR
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, 
                    font_name=Game.FONTS, font_size=12, color=info_color)
        if self.levelup_timer > 0:
            self.levelup_timer -= 1            
            self.draw_level_status(text=f'Level\n{self.level}', use_light=False)
                        
    def draw_level_status(self, text='Game\nOver', use_light=True):
        if(use_light): colors = Game.COLOR_LIST_LIGHT
        else: colors = Game.COLOR_LIST
        start_x = constants.SCREEN_WIDTH/2 - 40
        start_y = constants.SCREEN_HEIGHT * 3 / 5
        color = int(self._text_color_control % len(colors))
        color_2 = int(self._text_color_control * 7 % len(colors))
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_name=Game.FONTS,
                    font_size=20, color=colors[color], align='center')
        arcade.draw_rectangle_outline(start_x + 32, start_y + 28, 100, 60, colors[color_2])
        self._text_color_control += .05
    
    def draw_help_info(self, text, use_light=True):
        if text is None: text = '(Q)uit \n(S)tart'
        if(use_light): colors = Game.COLOR_LIST_LIGHT
        else: colors = Game.COLOR_LIST
        start_x = constants.SCREEN_WIDTH/2 - 38
        start_y = constants.SCREEN_HEIGHT * 1 / 8
        #color = int(self._text_color_control % len(colors))
        color = int(self._text_color_control * .3 % len(colors))
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=10, 
                    font_name=Game.FONTS, color=colors[color], align='center')
        
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
        self.background_angle += self._background_angle_control
        

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
                self.ship.brake()

            # Machine gun mode... bullet_regulator keeps the laser from 
            # firing every single frame.
            if arcade.key.SPACE in self.held_keys :
                if self.bullet_regulator > 0:
                    self.bullets.append(self.ship.fire())
                self.bullet_regulator *= -1
        else:    
            if not self.held_keys.isdisjoint(Game.START_KEYS):                
                self.restart()
            elif arcade.key.Q in self.held_keys:
                arcade.close_window()
                
    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)
        elif key in Game.GAME_OVER_KEYS:
            self.held_keys.add(key)

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
            self.rock_count += 1
            # OR?
            self.update_rate += 5
            self.set_update_rate(float(1/self.update_rate))
            self.rocks.append(TimerRock())
            self.levelup_timer = 90
        elif (0 < len(self.rocks) < 3):
            if random.random() * Alien.APPEAR_CHANCE < 1:
                if(constants.DEBUG): print('\n\nUPDATE: !!! Alien  !!!\n\n')
                self.rocks.append(Alien())

                        
    def set_reset(self):
        """Sets up asteroid rocks and ship, separate method keeps update() clean."""
        self.reset = False
        random.seed()
        #generate rocks 
        if self.ship is None:
            self.ship = Ship()           
        rock = None           
        for r in range(self.rock_count):
            if self.ship is not None:
                rerock = True                 
                while (rerock):
                    point = Point((random.random() * constants.SCREEN_WIDTH), 
                            (random.random() * constants.SCREEN_HEIGHT))
                    rock = BigRock(point)
                    if not rock.is_near(self.ship):
                        rerock = False
            self.rocks.append(rock)
        
    def _advance_flyers(self, flyers):
        for flyer in flyers:
#            print(f'Asteroid: advancing flyer {flyer}')
            flyer.advance()
            
    def _check_flyer_collisions(self):
        """ check for collisions amongst the rocks for bullets, and ship"""
        """ Where the flyers are added from the collection."""
        # create a temp collection to hold the created rocks during this process.
        new_rocks = []
        new_bullets = []
        for rock in self.rocks:
            for bullet in self.bullets:
                temp_rocks = None
                if (rock.is_near(bullet)):
                    self.score += rock.points
                    if (constants.DEBUG): 
                        print(f'debug: game._check_flyer_collisions: {bullet}')
                    new_rocks.extend(rock.split())
                    rock.alive = False
                    bullet.alive = False
                    #Both rock/bullet will be removed
                    # during zombie check.                    
                    break;  #break
                    # why break and not continue? break stops all bullets for this dead rock
                    # continue just stops this iteration.
                if (self.ship.alive and self.ship.is_near(bullet)):
                    # both aliens and ships can be harmed by their own bullets.
                    bullet.alive = False
                    self.ship.hit(bullet)
                    break;  #out of this iteration of bullet (it's dead)
                    
                    
            if self.ship.alive and rock.is_near(self.ship):
                if (constants.DEBUG):
                    print(f'\n\ndebug: game._check_flyer_collisions: SHIP HAS BEEN HIT {self.ship}\n\n')
                    print(f'debug: game._check_flyer_collisions: {rock}')
                # this will invoke shields if appropriate
                self.ship.hit(rock) 
                new_rocks.extend(rock.split())
                self.score += rock.points
                rock.alive = False        
                break;
            if isinstance(rock, Alien):
                # chance to fire a bullet at the ship
                if random.random() * Alien.FIRE_CHANCE < 1:
                    # # as there is no rock.fire(), going to add this funcitonality here.                    
                    # angle = math.atan2(self.ship.center.y - rock.center.y, self.ship.center.x - rock.center.x)
                    # angle = angle * 180/math.pi  #convert to degrees
                    # # create new instances of point and velocity
                    # p = Point(rock.center.x, rock.center.y)
                    # v = Velocity(rock.velocity.dx, rock.velocity.dy)
                    # aBullet = AlienBullet(p, angle, v)
                    aBullet = rock.fire(self.ship)
                    if(constants.DEBUG): print('_check_flyer_col: new alien bullet:', aBullet)
                    #new_rocks.append(aBullet)
                    new_bullets.append(aBullet)
        # now add new_rocks set to the mix:
        if len(new_rocks) > 0 : 
            self.rocks.extend(new_rocks)
        if len(new_bullets) > 0:
            self.bullets.extend(new_bullets)
        
            
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
        """Removes zombies"""
        # using list comprehensions to create new lists 
        # rather than removing from the middle several times
        self.rocks = [rock for rock in self.rocks if rock.alive]                
        self.bullets = [bullet for bullet in self.bullets if bullet.alive]
        # Tried two different approaches. Switching out sets/lists
        # seemed faster than removing the elements.
        # going with lists so no ghosting asteroid effect 
    def _wrap_flyer(self, flyer):
        """
        manipulates a flyer's center point to wrap around the arcade window
        """
        # This method will only adjust a center if the flyer
        # has truly crossed the halfway point.
        if flyer.center.x - flyer.radius > constants.SCREEN_WIDTH:
            flyer.center.x -= constants.SCREEN_WIDTH + 2*flyer.radius
        elif flyer.center.x + flyer.radius < 0:
            flyer.center.x += constants.SCREEN_WIDTH + 2*flyer.radius
            # now for y:
        if flyer.center.y - flyer.radius > constants.SCREEN_HEIGHT:
            flyer.center.y -= constants.SCREEN_HEIGHT + 2*flyer.radius
        elif flyer.center.y + flyer.radius < 0:
            flyer.center.y += constants.SCREEN_HEIGHT + 2*flyer.radius
            
                    
# Creates the game and starts it going
window = Game(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
arcade.run()
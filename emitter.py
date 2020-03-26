

"""
Particle Systems: emitter
Based on the Python Arcade Emitter Demo
"""
import arcade
from arcade.examples.frametime_plotter import FrametimePlotter
import pyglet
import os
import random
import math
import constants

QUIET_BETWEEN_SPAWNS = 0.25  # time between spawning another particle system
EMITTER_TIMEOUT = 10 * 60
# CENTER_POS = (constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
BURST_PARTICLE_COUNT = 500
TEXTURE = ":resources:images/pinball/pool_cue_ball.png"
TEXTURE2 = ":resources:images/space_shooter/playerShip3_orange.png"
TEXTURE3 = ":resources:images/pinball/bumper.png"
TEXTURE4 = ":resources:images/enemies/wormGreen.png"
TEXTURE5 = ":resources:images/space_shooter/meteorGrey_med1.png"
TEXTURE6 = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
TEXTURE7 = ":resources:images/tiles/boxCrate_double.png"
DEFAULT_SCALE = 0.20 # 0.3
DEFAULT_ALPHA = 27 #32
DEFAULT_PARTICLE_LIFETIME = 0.6 #3.0
PARTICLE_SPEED_FAST = 1.0
PARTICLE_SPEED_SLOW = 0.3
DEFAULT_EMIT_INTERVAL = 0.003
DEFAULT_EMIT_DURATION = 0.40

class ParticleBurst:
    def __init__(self, center_pos, velocity=None):
        self.emitter_timeout = 0
        if velocity:
            self.speed = PARTICLE_SPEED_FAST + velocity.speed
        else:
            self.speed = PARTICLE_SPEED_FAST
        self.frametime_plotter = FrametimePlotter()
        self.emitter = arcade.Emitter(
            center_xy=center_pos,
            emit_controller=arcade.EmitBurst(BURST_PARTICLE_COUNT),
            # emit_controller=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=TEXTURE,
                change_xy=arcade.rand_on_circle((0.0, 0.0), self.speed),
                lifetime=random.uniform(DEFAULT_PARTICLE_LIFETIME - 0.5, DEFAULT_PARTICLE_LIFETIME),
                #lifetime=DEFAULT_PARTICLE_LIFETIME,
                scale=DEFAULT_SCALE,
                alpha=DEFAULT_ALPHA
            )
        )
        
    def draw(self):
        if self.emitter:
            self.emitter.draw()
        
    def advance(self, delta_time):
        if self.emitter:
            self.emitter_timeout += 1
            self.emitter.update()
            if self.emitter.can_reap() or self.emitter_timeout > EMITTER_TIMEOUT:
                self.frametime_plotter.add_event("reap")
                #pyglet.clock.schedule_once(self.next_emitter, QUIET_BETWEEN_SPAWNS)
                self.emitter = None
        self.frametime_plotter.end_frame(delta_time)
    
    @property
    def alive(self):
        is_alive = False
        if self.emitter:
            is_alive = True
        return is_alive
    

#p = ParticleBurst((constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2))
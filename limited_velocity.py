"""
File: limited_velocity.py
Author: Mark Tobler

Re-imagines Velocity as a Property based class, and extends it to introduce
limits.
    max_speed : float
    max_acceleration (which is max_speed squared, so @property) 
    dx ()  : property
    dx (x) : property setter
    dy ()  : property
    dy (y) : property setter
    _dx : float 
    _dy : float
    __init__()
"""
from math import sqrt, pow, tan, atan, sin, cos, pi
import constants
from velocity import Velocity
from point import Point


class LimitedVelocity(Velocity):
  """
  Re-imagines Velocity as a Property based class, and extends it to 
  introduce limits.  max_speed should be defined before dx and dy, 
  otherwise, they'll end up limited by default max_speed
  """
  MAX_SPEED_DEFAULT = 20
  
  def __init__(self, dx=0.0, dy=0.0, max_speed = MAX_SPEED_DEFAULT):
    # not calling super just yet
    self.max_speed = max_speed
    # engine is insisting I add this. Tho, there's no such 
    # requirement for dx. Why? Must be because _dy is used
    self._dy = 0.0
    self.dx = dx
    self.dy = dy
  
  @property  
  def dx(self):
    return self._dx
  
  @property
  def dy(self):
    return self._dy
  
  @dx.setter
  def dx(self, dx):
    """
    can't be over max_speed. dx^2 together with dy^2 cannot be over max_speed^2
    """
    # however, speed is scalar. Need to compute using dy
    if (pow(dx,2) + pow(self._dy,2)  > pow(self.max_speed,2)):
      # preserving polarity by dividing dx with its absolute value 
      self._dx = sqrt(pow(self.max_speed,2) - pow(self._dy,2)) * dx/abs(dx)
    else:
      self._dx = dx
    
  @dy.setter
  def dy(self, dy):
    """
    can't be over max_speed. dy^2 together with dx^2 cannot be over max_speed^2
    """
    # speed is scalar. Need to compute using dx
    if (pow(dy,2) + pow(self._dx,2)  > pow(self.max_speed,2)):
      self._dy = (sqrt(pow(self.max_speed,2) - pow(self._dx,2))) * dy/abs(dy)
    else:
      self._dy = dy
    
  def set_velocity(self, dx, dy):
    """
    Helper Method to set dx and dy when replacing values individually 
    causes loss in precision due to limits. 
    """
    # using Pythagorean theorem to assess if limiting should take place.
    if (pow(dx,2) + pow(dy,2) > pow(self.max_speed,2)):
      # rather than fail, divide max_speed up by ratio of dx to dy
      if (constants.DEBUG): print(f'limited_velocity: set_velocity: attempted to set speed to :{sqrt(pow(dx, 2)+pow(dy,2))}')
      # the values of dx and dy are squared, added together and, de-squared 
      # to form a working ratio when adjusting speed at the limit.
      self._dx = self.max_speed * (dx/sqrt(pow(dy, 2) + pow(dx,2)))
      self._dy = self.max_speed * (dy/sqrt(pow(dy, 2) + pow(dx,2)))
      if (constants.DEBUG): print(f'       debug:(set to):{self}')
    else:
      self._dx = dx
      self._dy = dy
    
      
# #Testing
# v = LimitedVelocity(5, 5, 30)
# print(v)
# p = Point(1,1)
# print(p)
# p = p+v
# print(p)
# print(v.speed)
# v.dx = 30
# print(v)
# v.dy = 30
# print(v)
# print(v.set_velocity(15,25))
# print(v)
# print(v.speed)
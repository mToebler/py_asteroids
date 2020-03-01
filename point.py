"""
File: point.py
Author: Mark Tobler
Contains: Point and WrappingPoint
Encapsulates the concept of a point in 2-D space, or a quadrant of a 
Cartesian plane
  From the UML:
    x : float
    y : float
    __init__()
"""
from velocity import Velocity
import constants

class Point:
    """Simple point class (x,y) comparable"""
    #static constants
    
    #@property
    @classmethod
    def LOW_POINT(cls):
        return Point(0.0,0.0)
    
    def __init__(self, x=0.0, y=0.0):
        """initializer. if no values specified, defaulting to (0.0,0.0)"""
        self.x = x
        self.y = y

    def __repr__(self):
        """for printing and such. How Velocity represents itsefl textually"""
        return str(f'({self.x}, {self.y})')

    def __add__(self, other):
        """for adding points, velocities, ints and floats together via +"""
        # creating a copy of self, and returning modifications to that
        # so evaluations can be done. For example:
        #   if point_x == point + another_point
        # won't change the actual point, but can by captured
        # on the LHS of the assignment operator: 
        #   point = point + another_point
        return_point = Point(self.x, self.y)
        
        if isinstance(other, Point):
            return_point.x += other.x
            return_point.y += other.y
        elif isinstance(other, Velocity):
            return_point.x += other.dx
            return_point.y += other.dy
        elif type(other) == int or float:
            # treating like it's squared.
            return_point.x += other
            return_point.y += other
        # self is unchanged.
        return return_point
        
    def __sub__(self, other):
        """Subtraction, -, supported for Point, Velocity, int, float"""
        return_point = Point(self.x, self.y)
        
        if type(other) == Point:            
            return_point.x = return_point.x - other.x
            return_point.y = return_point.y - other.y
        elif type(other) == Velocity:
            return_point.x -= other.dx
            return_point.y -= other.dy
        elif type(other) == int or float:
            # treating like it's squared.
            return_point.x -= other
            return_point.y -= other
        # self is unchanged.
        return return_point
        
    def __mul__(self, other):
        """multiplication, *, support for Point, Velocity, int, float"""
        return_point = Point(self.x, self.y)
        
        if type(other) == Point:
            return_point.x *= other.x
            return_point.y *= other.y
        elif type(other) == Velocity:
            return_point.x *= other.dx
            return_point.y *= other.dy
        elif type(other) == int or float:
            # treating like it's squared.
            return_point.x *= other
            return_point.y *= other
        # self is unchanged.
        return return_point
        
            
    def move_by(self, velocity):
        """
        Will move by the provided vector value (a Velocity|dx & dy attributes)
        """
        if isinstance(velocity, Velocity):
            self.x += velocity.dx
            self.y += velocity.dy
        else:
            print(f'point: move_by: {type(velocity)}not a velocity object.')
        return self
    
    #implementing the rich comparison operators
    def __lt__(self, other):
        return True if self.x < other.x else True if self.y < other.y else False

    def __le__(self, other):
        return self < other or self == other
        # let's hear it for the double nested ternary!
        #return True if self.x < other.x else True if self.y < other.y else True if (self.x == other.x and self.y == other.y) else False

    def __gt__(self, other):        
        return True if self.x > other.x else True if self.y > other.y else False
    
    def __ge__(self, other):
        return self > other or self == other
        # once more with nested-ternary passion!
        #return True if self.x > other.x else True if self.y > other.y else True if (self.x == other.x and self.y == other.y) else False
    
    def __eq__(self, other):
        return ((self.x, self.y) == (other.x, other.y))
    
    def __ne__(self, other):
        return (not(self == other))



# class WrappingPoint(Point):
#     """
#     A Point that wraps around established limits
#     """
#     def __init__(self, x=0.0, y=0.0, limit_x=constants.SCREEN_WIDTH, limit_y=constants.SCREEN_HEIGHT):
#         self.limit_x = limit_x
#         self.limit_y = limit_y
#         super().__init__(x,y)
#         self._x = x
#         self._y = y
# #        self.x = x
# #        self.y = y
    
#     @property
#     def x(self):
#         return self._x
    
#     @x.setter
#     def x(self, x):
#         if (x > self.limit_x):
#             self._x = x - self.limit_x
#         elif (x < 0):
#             self._x = x + self.limit_x
            
#     @property
#     def y(self):
#         return self._y
    
#     @y.setter
#     def y(self, y):
#         if (y > self.limit_y):
#             self._y = y - self.limit_y
#         elif (y < 0):
#             self._y = y + self.limit_y
        
    # now the big test is to see if it inherits Point's methods properly.
        
#testing
# wp = WrappingPoint(20, 30)
# p = WrappingPoint(2, 3)
# wp = p + wp
# print(wp)            
            
            
            
#testing
# point = Point(1,1)
# v = Velocity(1.1, 2.2)
# print(point, v)
# point = point + v
# print(point)
# point = point + Point(-1,-2)
# print(point)
# p = Point(1,2)
# p2 = Point(3.1, 4.2)
# print(p * p2)
# print(p2*p2)


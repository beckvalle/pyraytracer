from math import sqrt

# implement raytracer using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

# vec3 class - basis for points and colors
class vec3():

    # initilize class
    def __init__(self, e0:float=None, e1:float=None, e2:float=None):
        if None not in [e0, e1, e2]:  # fill all values if 3 values given
            self._e = [e0, e1, e2]
        elif e0 is not None:  # fill all values with 1st if 1st value given
            if isinstance(e0, vec3):
                self._e = e0._e
            else:
                self._e = [e0, e0, e0]
        else: # fill all values with 0 if no value given
            self._e = [0, 0, 0]

    # create a nice format for printing
    def __str__(self):
        return "({0}, {1}, {2})".format(self._e[0], self._e[1], self._e[2])
        
    def __getitem__(self, index):
        return self._e[index]
    
    def __getattr__(self, attr):
        if attr in ['x', 'y', 'z', 'len_sqr', 'len']:
            if attr == 'x':
                return self._e[0]
            elif attr == 'y':
                return self._e[1]
            elif attr == 'z':
                return self._e[2]
            elif attr == 'len_sqr':
                return self._e[0]*self._e[0]+self._e[1]*self._e[1]+self._e[2]*self._e[2]
            elif attr == 'len':
                return sqrt(self._e[0]*self._e[0]+self._e[1]*self._e[1]+self._e[2]*self._e[2])
        else:
            raise AttributeError("%r object has no attribute %r" %
                             (self.__class__.__name__, attr))

    def __neg__(self):
        return vec3(-self._e[0], -self._e[1], -self._e[2])

    def __eq__(self, other):
        if type(self) is type(other):
            return self._e == other._e
        return False
        
    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True

    def __add__(self, other):
        if isinstance(other, vec3):
            e0 = self._e[0] + other._e[0]
            e1 = self._e[1] + other._e[1]
            e2 = self._e[2] + other._e[2]
            return vec3(e0, e1, e2)
        else:
            raise TypeError()
            
    def __mul__(self, operand):
        e0 = self._e[0] * operand
        e1 = self._e[1] * operand
        e2 = self._e[2] * operand
        return vec3(e0, e1, e2)
    
    def __truediv__(self, operand):
        if operand != 0:
            e0 = self._e[0] * (1/operand)
            e1 = self._e[1] * (1/operand)
            e2 = self._e[2] * (1/operand)
            return vec3(e0, e1, e2)
        else:
            raise ZeroDivisionError()

# create class alias for point3 and color
point3 = vec3
color = vec3

# utility functions for vec3
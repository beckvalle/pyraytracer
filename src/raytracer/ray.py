# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

from src.raytracer import raytracer

# ray class
# a ray has point origin, a vector direction, and a time
# args: origin - ray origin, direction, ray direction its pointing at, time - time
class ray():
    def __init__(self, origin=None, direction=None, time=0.0):
        # check origin arg is valid
        if isinstance(origin, raytracer.point3) or origin is None:
            self.origin = origin
        else:
            raise TypeError()
        # check direction arg is valid
        if isinstance(direction, raytracer.vec3) or origin is None:
            self.direction = direction
        else:
            raise TypeError()
        # check time is valid
        if isinstance(time, float):
            self.time = time
        else:
            raise TypeError()

    # used to print nicely
    def __str__(self):
        return "("+str(self.origin)+', '+str(self.direction)+' at '+str(self.time)+')'

    # calculates position at time
    # arg: t = float of time
    # returns: position at time
    def at(self, t):
        # makes sure origin and direction are set and time is valid
        if self.origin is None or self.direction is None:
            raise AttributeError()
        if not isinstance(t, float):
            raise TypeError()
        
        # calculates position at time
        return self.origin + t * self.direction
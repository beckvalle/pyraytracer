# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

from src.raytracer import raytracer

# ray class
class ray():
    def __init__(self, origin=None, direction=None):
        if None not in [origin, direction]:
            self.origin = raytracer.point3(origin)
            self.direction = raytracer.vec3(direction)
        else:
            self.origin = None
            self.direction = None
        
    def at(self, t):
        return self.origin + t * self.direction
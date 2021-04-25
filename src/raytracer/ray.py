# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

from src.raytracer import raytracer

# ray class
class ray():
    def __init__(self, origin=None, direction=None):
        if isinstance(origin, raytracer.point3) or origin is None:
            self.origin = origin
        else:
            raise TypeError()

        if isinstance(direction, raytracer.vec3) or origin is None:
            self.direction = direction
        else:
            raise TypeError()

    def at(self, t):
        if self.origin is None or self.direction is None:
            raise AttributeError()
        if not isinstance(t, float):
            raise TypeError()

        return self.origin + t * self.direction
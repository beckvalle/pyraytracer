# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

from src.raytracer import raytracer
from src.raytracer.ray import ray

# camera class
class camera():
    def __init__(self, origin=None, direction=None):
        self.aspect_ratio = 16.0 / 9.0
        self.viewport_height = 2.0
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.0
        self.origin = raytracer.point3(0, 0, 0)
        self.horizontal = raytracer.vec3(self.viewport_width, 0.0, 0.0)
        self.vertical = raytracer.vec3(0.0, self.viewport_height, 0.0)
        self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - raytracer.vec3(0, 0, self.focal_length)

    def get_ray(self, u, v):
        if not isinstance(u, float):
            raise TypeError()
        if not isinstance(v, float):
            raise TypeError()
            
        return ray(self.origin, self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)
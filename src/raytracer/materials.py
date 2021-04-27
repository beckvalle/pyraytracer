# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

from abc import ABC, abstractmethod
from src.raytracer import rweekend
from src.raytracer import raytracer
from src.raytracer import ray
from src.raytracer import hittables
from src.raytracer.raytracer import random_unit_vector

# material class
class material(ABC):

    @abstractmethod
    def scatter(self, r_in, rec, attenuation, scattered):
        pass

class lambertian(material):
    def __init__(self, albedo):
        if isinstance(albedo, raytracer.color):
            self.albedo = albedo
        else:
            raise TypeError()

    def scatter(self, r_in, rec, attenuation, scattered, seed=None):
        if not isinstance(r_in, ray.ray):
            raise TypeError()
        if not isinstance(rec, hittables.hit_record):
            raise TypeError()
        if not isinstance(attenuation, raytracer.color):
            raise TypeError()
        if not isinstance(scattered, ray.ray):
            raise TypeError()
    
        scatter_direction = rec.normal + random_unit_vector(seed)
        if (scatter_direction.near_zero()):
            scatter_direction = rec.normal

        scattered = ray.ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True
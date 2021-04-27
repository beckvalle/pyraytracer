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
    def scatter(self, r_in, rec, attenuation, scattered, seed=None):
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
        return (True, scattered, attenuation)

class metal(material):
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

        reflected = raytracer.reflect(raytracer.unit(r_in.direction), rec.normal)
        scattered =  ray.ray(rec.p, reflected)
        attenuation = self.albedo
        out = raytracer.dot(scattered.direction, rec.normal) > 0
        return (out, scattered, attenuation)
        
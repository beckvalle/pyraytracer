# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

from abc import ABC, abstractmethod
from src.raytracer import rweekend
from src.raytracer import raytracer
from src.raytracer import ray
from src.raytracer import hittables
from src.raytracer.raytracer import random_unit_vector, random_in_unit_sphere
from math import sqrt

# abstract base material class
class material(ABC):

    @abstractmethod
    def scatter(self, r_in, rec, attenuation, scattered, seed=None):
        pass

# class for lambertian materials - not very reflective
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

        scattered = ray.ray(rec.p, scatter_direction, r_in.time)
        attenuation = self.albedo
        return (True, scattered, attenuation)

# class for metalic materials - can be shinny or matte (set fuzz)
class metal(material):
    def __init__(self, albedo, fuzz=1.0):
        if isinstance(albedo, raytracer.color):
            self.albedo = albedo
        else:
            raise TypeError()
        if isinstance(fuzz, float):
            if fuzz > 1.0:
                fuzz = 1.0
            self.fuzz = float(fuzz)
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
        scattered =  ray.ray(rec.p, reflected + self.fuzz * random_in_unit_sphere(), r_in.time)
        attenuation = self.albedo
        out = raytracer.dot(scattered.direction, rec.normal) > 0
        return (out, scattered, attenuation)

# class for glass type materials
class dielectric(material):
    def __init__(self, index_of_refraction):
        if isinstance(index_of_refraction, float):
            self.ir = index_of_refraction
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
        
        attenuation = raytracer.color(1.0, 1.0, 1.0)
        refraction_ratio = 1.0/self.ir if rec.front_face else self.ir
        unit_direction = raytracer.unit(r_in.direction)
        # print ('unit_direction: ', unit_direction)
        
        cos_theta = min(raytracer.dot(-unit_direction, rec.normal), 1.0)
        # print ('cos theta: ', cos_theta)
        sin_theta = sqrt(1.0 - (cos_theta * cos_theta))
        # print ('sin theta: ', sin_theta)
        cannot_refract = (refraction_ratio * sin_theta > 1.0)
        
        if cannot_refract or (self.reflectance(cos_theta, refraction_ratio) > rweekend.random_double()):
            direction = raytracer.reflect(unit_direction, rec.normal)
        else:
            direction = raytracer.refract(unit_direction, rec.normal, refraction_ratio)
            
        scattered = ray.ray(rec.p, direction, r_in.time)
        
        return (True, scattered, attenuation)
    
    def reflectance(self, cosine, ref_idx):
        if not isinstance(cosine, float):
            raise TypeError()
        if not isinstance(ref_idx, float):
            raise TypeError()
        
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0
        return r0 + (1 - r0) * pow((1 - cosine), 5)
        
from src.raytracer import raytracer
from abc import ABC, abstractmethod
from src.raytracer import ray
import math

class hit_record():
    def __init__(self, p, normal, t):
        if isinstance(p, raytracer.point3):
            self.p = p
        else:
            raise TypeError()
        if isinstance(normal, raytracer.vec3):
            self.normal = normal
        else:
            raise TypeError()
        if isinstance(t, float):
            self.t = t
        else:
            raise TypeError()

class hittable(ABC):
    @abstractmethod
    def hit(self, r, t_min, t_max, rec):
        if not isinstance(r, ray.ray):
            raise TypeError()
        if not isinstance(t_min, float):
            raise TypeError()
        if not isinstance(t_max, float):
            raise TypeError()
        if not isinstance(rec, hit_record):
            raise TypeError()

class sphere(hittable):
    def __init__(self, center=None, radius=None):
        if isinstance(center, raytracer.point3) or center is None:
            self.center = center
        else:
            raise TypeError()
        if isinstance(radius, float) or radius is None:
            self.radius = radius
        else:
            raise TypeError()

    def hit(self, r, t_min, t_max, rec):
        if self.center == None or self.center == None:
            raise AttributeError()
        if not isinstance(r, ray.ray):
            raise TypeError()
        if r.origin == None or r.direction == None:
            raise AttributeError()
        if not isinstance(t_min, float):
            raise TypeError()
        if not isinstance(t_max, float):
            raise TypeError()
        if not isinstance(rec, hit_record):
            raise TypeError()

        oc = r.origin - center
        a = r.direction.len_sqr
        half_b = dot(oc, r.direction)
        c = oc.len_sqr - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return False
        sqrtd = math.sqrt(discriminant)
        
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False
        
        rec.t = root
        rec.p = r.at(rec.t)
        rec.normal = rec.p - center / radius
        
        return True
        
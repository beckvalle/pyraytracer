from src.raytracer import raytracer
from abc import ABC, abstractmethod
from src.raytracer import ray
from src.raytracer.raytracer import dot
import math

class hit_record():
    def __init__(self, p=None, normal=None, t=None):
        if isinstance(p, raytracer.point3) or p is None:
            self.p = p
        else:
            raise TypeError()
        if isinstance(normal, raytracer.vec3) or normal is None:
            self.normal = normal
        else:
            raise TypeError()
        if isinstance(t, float) or t is None:
            self.t = t
        else:
            raise TypeError()
        self.front_face = None
        
    def set_face_normal(self, r, outward_normal):
        if not isinstance(r, ray.ray):
            raise TypeError()
        if not isinstance(outward_normal, raytracer.vec3):
            raise TypeError()

        self.front_face = dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class hittable(ABC):
    @abstractmethod
    def hit(self, r, t_min, t_max, rec):
        if not isinstance(r, ray.ray) and r is not None:
            raise TypeError()
        if not isinstance(t_min, float) and t_min is not None:
            raise TypeError()
        if not isinstance(t_max, float) and t_max is not None:
            raise TypeError()
        if not isinstance(rec, hit_record) and rec is not None:
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
        if self.center == None or self.radius == None:
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

        oc = r.origin - self.center
        a = r.direction.len_sqr
        half_b = dot(oc, r.direction)
        c = oc.len_sqr - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return (False, None)
        sqrtd = math.sqrt(discriminant)
        
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return (False, None)
        
        rec.t = root
        rec.p = r.at(rec.t)
        rec.outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, rec.outward_normal)
        
        return (True, rec)

class hittable_list(hittable):
    def __init__(self, h_object=None):
        self.objects = []
        if isinstance(h_object, hittable) or h_object is None:
            if isinstance(h_object, hittable):
                self.objects.append(h_object)
        else:
            raise TypeError()

    def clear(self):
        self.objects = []

    def add(self, h_object):
        self.objects.append(h_object)

    def hit(self, r, t_min, t_max, rec):
        if not isinstance(r, ray.ray):
            raise TypeError()
        if not isinstance(t_min, float):
            raise TypeError()
        if not isinstance(t_max, float):
            raise TypeError()
        if not isinstance(rec, hit_record):
            raise TypeError()

        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max

        for h_obj in self.objects:
            hit_out = h_obj.hit(r, t_min, closest_so_far, temp_rec)
            if hit_out[0]:
                hit_anything = True
                closest_so_far = hit_out[1].t
                temp_rec = hit_out[1]

        return (hit_anything, temp_rec)
        
   
from src.raytracer import raytracer
from abc import ABC, abstractmethod
from src.raytracer import ray, materials, aabbs
from src.raytracer.raytracer import dot
from src.raytracer import rweekend
import math
from functools import cmp_to_key

# container class for keeping track of hit information
class hit_record():
    def __init__(self, p=None, normal=None, material=None, t=None, u=None, v=None):
        # check args are valid
        if isinstance(p, raytracer.point3) or p is None:
            self.p = p
        else:
            raise TypeError()
        if isinstance(normal, raytracer.vec3) or normal is None:
            self.normal = normal
        else:
            raise TypeError()
        if isinstance(material, materials.material) or material is None:
            self.material = material
        else:
            raise TypeError()
        if isinstance(t, float) or t is None:
            self.t = t
        else:
            raise TypeError()

        # u and v are surface texture coordinates
        if isinstance(u, float) or u is None:
            self.u = u
        else:
            raise TypeError()
        if isinstance(v, float) or v is None:
            self.v = v
        else:
            raise TypeError()
        self.front_face = None
        
    # print string for debugging
    def __str__(self):
        return("HR p: "+str(self.p)+" n: "+str(self.normal)+" mat: "+str(self.material)
               +" t: "+str(self.t)+" u: "+str(self.u)+" v: "+str(self.v)+" ff: "+str(self.front_face)+"\n")
        
    def set_face_normal(self, r, outward_normal):
        if not isinstance(r, ray.ray):
            raise TypeError()
        if not isinstance(outward_normal, raytracer.vec3):
            raise TypeError()

        self.front_face = dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

# abstract base class for things that can be hit
class hittable(ABC):
    # abstract method - needs to be implemented in all child classes
    @abstractmethod
    def hit(self, r, t_min, t_max, rec):
        # check args are valid
        if not isinstance(r, ray.ray) and r is not None:
            raise TypeError()
        if not isinstance(t_min, float) and t_min is not None:
            raise TypeError()
        if not isinstance(t_max, float) and t_max is not None:
            raise TypeError()
        if not isinstance(rec, hit_record) and rec is not None:
            raise TypeError()

    # abstract method for hitting bounding box
    @abstractmethod
    def bounding_box(self, time0, time1):
        pass

# class for spheres
class sphere(hittable):
    def __init__(self, center=None, radius=None, material=None):
        # check args are valid
        if isinstance(center, raytracer.point3) or center is None:
            self.center = center
        else:
            raise TypeError()
        if isinstance(radius, float) or radius is None:
            self.radius = radius
        else:
            raise TypeError()
        if isinstance(material, materials.material) or material is None:
            self.material = material
        else:
            raise TypeError()

    # determine if hit
    def hit(self, r, t_min, t_max, rec):
        # check args are valid
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
        
        # used to find nearest root in acceptable range
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return (False, None)
        
        rec.t = root
        rec.p = r.at(rec.t)
        rec.outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, rec.outward_normal)
        uv_out = self.get_sphere_uv(rec.outward_normal)
        rec.u = uv_out[0]
        rec.v = uv_out[1]
        rec.material = self.material
        
        return (True, rec)

    def bounding_box(self, time0, time1):
        # check args are valid
        if not isinstance(time0, float):
            raise TypeError()
        if not isinstance(time1, float):
            raise TypeError()

        # construct bounding box from radius
        output_box = aabbs.aabb(
            self.center - raytracer.vec3(self.radius, self.radius, self.radius),
            self.center + raytracer.vec3(self.radius, self.radius, self.radius))
        
        return output_box
    
    # function to return texture coords for sphere
    def get_sphere_uv(self, p):
        # check args
        if not isinstance(p, raytracer.point3):
            raise TypeError()
            
        # p is a given point on a sphere radius 1 centered on origin
        # u = returned value in [0, 1] of angle around y axis from x=-1
        # v = returned value in [0, 1] of angle from y=-1 to y=+1
        
        theta = math.acos(-p.y)
        phi = math.atan2(-p.z, p.x)+ rweekend.pi
        
        u = phi / (2 * rweekend.pi) 
        v = theta / rweekend.pi
        
        return (u, v)
        

# class for multiple hittable things
class hittable_list(hittable):
    def __init__(self, h_object=None):
        # container that holds objects
        self.objects = []
        
        # check args are valid
        if isinstance(h_object, hittable) or h_object is None:
            if isinstance(h_object, hittable):
                self.objects.append(h_object)
        else:
            raise TypeError()

    # empty the hittable object list
    def clear(self):
        self.objects = []

    # add hittable object to the list
    def add(self, h_object):
        self.objects.append(h_object)
    
    # export size
    def size(self):
        return len(self.objects)

    # function to check if any objects in list were hit
    def hit(self, r, t_min, t_max, rec):
        # check args are valid
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

    def bounding_box(self, time0, time1):
        # check args are valid
        if not isinstance(time0, float):
            raise TypeError()
        if not isinstance(time1, float):
            raise TypeError()

        # no bounding box if no objects
        if self.objects == []:
            return (False, None)

        # construct bounding box from objects
        temp_box = None
        first_box = True
        output_box = None
        
        for obj in self.objects:
            temp_box = obj.bounding_box(time0, time1)
            if not temp_box:
                return None
            output_box = temp_box if first_box else aabbs.surrounding_box(output_box, temp_box)
            
        return output_box

# class for spheres that move
# sphere center moves from cen0 at time0 to cen1 at time1
# r - radius, m - material
class moving_sphere(hittable):
    def __init__(self, cen0=None, cen1=None, _time0=None, _time1=None, r=None, m=None):
        # check args are valid
        if isinstance(cen0, raytracer.point3) or cen0 is None:
            self.center0 = cen0
        else:
            raise TypeError()
        if isinstance(cen1, raytracer.point3) or cen1 is None:
            self.center1 = cen1
        else:
            raise TypeError()
        if isinstance(_time0, float) or _time0 is None:
            self.time0 = _time0
        else:
            raise TypeError()
        if isinstance(_time1, float) or _time1 is None:
            self.time1 = _time1
        else:
            raise TypeError()
        if isinstance(r, float) or r is None:
            self.radius = r
        else:
            raise TypeError()
        if isinstance(m, materials.material) or m is None:
            self.material = m
        else:
            raise TypeError()

    # determine center position at time
    def center(self, time):
        return (self.center0 
                + ((time - self.time0) / (self.time1 - self.time0))
                * (self.center1 - self.center0))
    
    # determine if hit
    def hit(self, r, t_min, t_max, rec):
        # check args are valid
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

        oc = r.origin - self.center(r.time)
        a = r.direction.len_sqr
        half_b = dot(oc, r.direction)
        c = oc.len_sqr - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return (False, None)
        sqrtd = math.sqrt(discriminant)
        
        # used to find nearest root in acceptable range
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return (False, None)
        
        rec.t = root
        rec.p = r.at(rec.t)
        rec.outward_normal = (rec.p - self.center(r.time)) / self.radius
        rec.set_face_normal(r, rec.outward_normal)
        rec.material = self.material
        
        return (True, rec)

    def bounding_box(self, time0, time1):
        # check args are valid
        if not isinstance(time0, float):
            raise TypeError()
        if not isinstance(time1, float):
            raise TypeError()

        # construct bounding box from radius
        box0 = aabbs.aabb(
            self.center(time0) - raytracer.vec3(self.radius, self.radius, self.radius),
            self.center(time0) + raytracer.vec3(self.radius, self.radius, self.radius))
        box1 = aabbs.aabb(
            self.center(time1) - raytracer.vec3(self.radius, self.radius, self.radius),
            self.center(time1) + raytracer.vec3(self.radius, self.radius, self.radius))
        output_box = aabbs.surrounding_box(box0, box1)
        
        return output_box

# class for bounding box nodes
class bvh_node(hittable):
    def __init__(self, hlist=None, _time0=None, _time1=None, src_objects=None, start=None, end=None):
        # check args
        if isinstance(hlist, hittable_list) or hlist is None:
            pass
        else:
            raise TypeError()
        if isinstance(_time0, float) or _time0 is None:
            self.time0 = _time0
        else:
            raise TypeError()
        if isinstance(_time1, float) or _time1 is None:
            self.time1 = _time1
        else:
            raise TypeError()
            
        if issubclass(type(src_objects), list) or src_objects is None:
            pass
        else:
            raise TypeError("error: type(src_objects) is "+str(type(src_objects)))
        if isinstance(start, int) or start is None:
            pass
        else:
            raise TypeError("error: start is "+str(type(start)))
        if isinstance(end, int) or end is None:
            pass
        else:
            
            raise TypeError("error: end is "+str(type(end)))
            
        # if hit list was passed in args
        if src_objects is None and hlist is not None:
            self.src_objects = hlist.objects
            self.start = 0
            self.end = len(hlist.objects)
        
        # if src_objects was passed in args
        if src_objects is not None:
            self.src_objects = src_objects
            self.start = start
            self.end = end
            
        # start constructor
        self.objects = self.src_objects
        axis = rweekend.random_int(0, 2, seed=None)
        if axis == 0:
            comparator = box_x_compare
        elif axis == 1:
            comparator = box_y_compare
        else:
            comparator = box_z_compare
            
        object_span = self.end - self.start
        
        if object_span == 1:
            self.left = self.objects[self.start]
            self.right = self.objects[self.start]
        elif object_span == 2:
            if comparator(self.objects[self.start], self.objects[self.start + 1]):
                self.left = self.objects[self.start]
                self.right = self.objects[self.start + 1]
            else:
                self.left = self.objects[self.start + 1]
                self.right = self.objects[self.start]
        else:
            self.objects[self.start:self.end] = sorted(self.objects[self.start:self.end], key=cmp_to_key(comparator))
            
            mid = math.floor(self.start + len(self.objects) / 2)
            self.left = bvh_node(src_objects=self.objects, start=self.start, end=mid, _time0=self.time0, _time1=self.time1)
            self.right = bvh_node(src_objects=self.objects, start=mid, end=self.end, _time0=self.time0, _time1=self.time1)
            
        box_left = self.left.bounding_box(self.time0, self.time1)
        box_right = self.right.bounding_box(self.time0, self.time1)
        
        if not box_left or not box_right:
            raise Error("No bounding box in node constructor.\n")
        
        self.box = aabbs.surrounding_box(box_left, box_right)

    # hit function      
    def hit(self, r, t_min, t_max, rec):
        if not isinstance(r, ray.ray):
            raise TypeError()
        if not isinstance(t_min, float):
            raise TypeError()
        if not isinstance(t_max, float):
            raise TypeError()
        if not isinstance(rec, hit_record):
            raise TypeError()
        
        if not self.box.hit(r, t_min, t_max):
            return (False, None)
        
        #temp_rec = hit_record()
        hit_anything = False
        
        # check both children nodes to see if they hit
        hit_out_left = self.left.hit(r, t_min, t_max, rec)
        if hit_out_left[0]:
            hit_anything = True
            rec = hit_out_left[1]
        hit_out_right = self.right.hit(r, t_min,
                                       rec.t if hit_out_left[0] else t_max, rec)
        if hit_out_right[0]:
            hit_anything = True
            rec = hit_out_right[1]

        return (hit_anything, rec)
        
    # bounding box function
    def bounding_box(self, time0, time1):
        return self.box
    
def box_compare(a, b, axis):
    if not isinstance(a, hittable):
        raise TypeError()
    if not isinstance(b, hittable):
        raise TypeError()
      
    box_a = a.bounding_box(0.0, 0.0)
    box_b = b.bounding_box(0.0, 0.0)
    if not box_a or not box_b:
        raise Error("No bounding box in node comparison constructor.\n")
        
    if box_a.minimum._e[axis] > box_b.minimum._e[axis]:
        return 1
    elif box_a.minimum._e[axis] < box_b.minimum._e[axis]:
        return -1
    else:
        return 0

def box_x_compare(a, b): 
    return box_compare(a, b, 0)

def box_y_compare(a, b): 
    return box_compare(a, b, 1)

def box_z_compare(a, b): 
    return box_compare(a, b, 2)

# class for rectangles
class xy_rect(hittable):
    def __init__(self, _x0, _x1, _y0, _y1, _k, mat):
        if isinstance(_x0, float) or _x0 is None:
            self.x0 = _x0
        else:
            raise TypeError()
        if not isinstance(_x1, float) or _x1 is not None:
            self.x1 = _x1
        else:
            raise TypeError()
        if not isinstance(_y0, float) or _y0 is not None:
            self.y0 = _y0
        else:
            raise TypeError()
        if not isinstance(_y1, float) or _y1 is not None:
            self.y1 = _y1
        else:
            raise TypeError()
        if not isinstance(_k, float) or _k is not None:
            self.k = _k
        else:
            raise TypeError()
        if isinstance(mat, materials.material) or mat is None:
            self.material = mat
        else:
            raise TypeError()
            
    def hit(self, r, t_min, t_max, rec):
        if not isinstance(r, ray.ray):
            raise TypeError()
        if not isinstance(t_min, float):
            raise TypeError()
        if not isinstance(t_max, float):
            raise TypeError()
        if not isinstance(rec, hit_record):
            raise TypeError()
            
        t = (self.k - r.origin.z) / r.direction.z
        if t < t_min or t > t_max:
            return (False, None)
        
        x = r.origin.x + t * r.direction.x
        y = r.origin.y + t * r.direction.y
        if (x < self.x0 or x > self.x1 or y < self.y0 or y > self.y1):
            return (False, None)
        
        #print("hit xyrec\n")
        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (y - self.y0) / (self.y1 - self.y0)
        rec.t = t
        rec.outward_normal = raytracer.vec3(0.0, 0.0, 1.1)
        rec.set_face_normal(r, rec.outward_normal)
        rec.material = self.material
        rec.p = r.at(t)
        #print("hit mat", rec.material, "\n")
        return (True, rec)
            
    # bounding box function
    def bounding_box(self, time0, time1):
        # pad z a small ammount so non zero
        return aabbs.aabb(raytracer.point3(self.x0, self.y0, self.k-0.0001), raytracer.point3(self.x1, self.y1, self.k+0.0001))
   
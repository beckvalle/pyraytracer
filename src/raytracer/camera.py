# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

from src.raytracer import raytracer
from src.raytracer.ray import ray
from src.raytracer import rweekend
import math

# camera class
# args:
# lookfrom - eye point
# lookat - point looking towards
# vup - vector of up position
# vfov - field of view
# aspect_ratio - aspect ratio per scene
# aperture - virtual camera aperture setting
# focus_dist - used to simulate focusing
# time0 - initial time for camera
# time1 - second time
class camera():
    def __init__(self, lookfrom=None, lookat=None, vup=None, vfov=None, aspect_ratio=(16.0 / 9.0), aperture=None, focus_dist=None, _time0=0.0, _time1=0.0):
        # check args are valid
        if isinstance(lookfrom, raytracer.point3) or lookfrom is None:
            pass
        else:
            raise TypeError()
        if isinstance(lookat, raytracer.point3) or lookat is None:
            pass
        else:
            raise TypeError()
        if isinstance(vup, raytracer.vec3) or vup is None:
            pass
        else:
            raise TypeError()

        if isinstance(vfov, float) or vfov is None:
            if vfov is None:
                self.viewport_height = 2.0
            else:
                theta = rweekend.degrees_to_radians(vfov)
                h = math.tan(theta / 2)
                self.viewport_height = 2.0 * h
        else:
            raise TypeError()

        if isinstance(aspect_ratio, float):
            self.aspect_ratio = aspect_ratio
        else:
            raise TypeError()
        if isinstance(aperture, float) or aperture is None:
            if aperture is not None:
                self.lens_radius = aperture / 2
            else:
                self.lens_radius = None
        else:
            raise TypeError()
        if isinstance(focus_dist, float) or focus_dist is None:
            pass
        else:
            raise TypeError()
        if isinstance(_time0, float):
            self.time0 = _time0
        else:
            raise TypeError()
        if isinstance(_time1, float):
            self.time1 = _time1
        else:
            raise TypeError()
        
        # set viewport and focal length
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.0
        
        # set camera settings
        if lookfrom is None or lookat is None or vup is None:
            # basic camera setings
            self.origin = raytracer.point3(0, 0, 0)
            self.horizontal = raytracer.vec3(self.viewport_width, 0.0, 0.0)
            self.vertical = raytracer.vec3(0.0, self.viewport_height, 0.0)
            self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - raytracer.vec3(0, 0, self.focal_length)
        else:
            # camera with look information suppied
            self.w = raytracer.unit(lookfrom - lookat)
            self.u = raytracer.unit(raytracer.cross(vup, self.w))
            self.v = raytracer.cross(self.w, self.u)
            
            self.origin = lookfrom
            
            # handle aperture and focus distance args
            if aperture is None or focus_dist is None:
                self.horizontal = self.viewport_width * self.u
                self.vertical = self.viewport_height * self.v
                self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - self.w
            else:
                self.horizontal = focus_dist * self.viewport_width * self.u
                self.vertical = focus_dist * self.viewport_height * self.v
                self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - focus_dist * self.w
                
    # create a camera ray
    def get_ray(self, s, t):
        if not isinstance(s, float):
            raise TypeError()
        if not isinstance(t, float):
            raise TypeError()
            
        if self.lens_radius:
            # implement focus blur
            rd = self.lens_radius * raytracer.random_in_unit_disk()
            offset = self.u * rd.x + self.v * rd.y
            return ray(self.origin + offset,  # ray origin
                       self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset,  # ray direction
                      rweekend.random_double(self.time0, self.time1))  # ray time
        else:
            # no blur
            return ray(self.origin,  # ray origin
                       self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin,  # ray direction
                      rweekend.random_double(self.time0, self.time1))  # ray time
    
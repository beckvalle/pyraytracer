# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingTheNextWeek.html#solidtextures

from src.raytracer import raytracer, rweekend
from src.raytracer import perlins
import math
from abc import ABC, abstractmethod
from PIL import Image  # image library
import sys

# texture class - base class for other textures to build from
class texture(ABC):
    
    # abstract method needs to be implemented by child classes
    @abstractmethod
    def value(self, u, v, p):
        # u and v are surface coordinates
        pass

class solid_color(texture):
    def __init__(self, c=None, red=None, green=None, blue=None):
        # check args
        if isinstance(c, raytracer.color):
            self.color_value = c
        elif isinstance(red, float) and isinstance(green, float) and isinstance(blue, float):
            self.color_value = raytracer.color(red, green, blue)
        else:
            raise TypeError()

    # check args and return value       
    def value(self, u, v, p):
        if not isinstance(p, raytracer.vec3):
            raise TypeError()

        # return simple color value
        return self.color_value 

# creates a checkerboard from 2 colors or tectures
class checker_texture(texture):
    def __init__(self, arg1=None, arg2=None):
        # check odds
        if isinstance(arg1, texture):
            self.even = arg1
        elif isinstance(arg1, raytracer.color):
            self.even = solid_color(arg1)
        else:
            raise TypeError()
        if isinstance(arg2, texture):
            self.odd = arg2
        elif isinstance(arg2, raytracer.color):
            self.odd = solid_color(arg2)
        else:
            raise TypeError()
            
    def value(self, u, v, p):
        # check args
        if not isinstance(p, raytracer.vec3):
            raise TypeError()
            
        sines = math.sin(10 * p.x) * math.sin(10 * p.y) * math.sin(10 * p.z)
        if sines < 0:
            return self.odd.value(u, v, p)
        else:
            return self.even.value(u, v, p)

# creates a random noise grey checker with initial perlin noise
class noise_texture(texture):
    def __init__(self):
        self.pnoise = perlins.perlin()
    
    def value(self, u, v, p):
        # check args
        if not isinstance(p, raytracer.vec3):
            raise TypeError()
            
        return raytracer.color(1.0, 1.0, 1.0) * self.pnoise.noise(p)

# maps an external image texture
class image_texture(texture):
    def __init__(self, filename=None):
        
        # try to load texture from file
        if filename:
            try:
                image = Image.open(filename)
                self.data = list(image.getdata())
                self.width, self.height = image.size
                                
            # image didn't load
            except:
                self.data = None 
                self.width = 0
                self.height = 0
                raise Error("ERROR: Could not load texture image file", filename, "\n")
        # no image given
        else:
            self.data = None
            self.width = 0
            self.height = 0

    def value(self, u, v, p):
        # check args
        if not isinstance(p, raytracer.vec3):
            raise TypeError()
            
        # if no image data return cyan
        if self.data is None:
            return color(0, 1, 1)
        
        # clamp texture coords to [0,1] by [1,0]
        u = rweekend.clamp(u, 0.0, 1.0)
        v = 1.0 - rweekend.clamp(v, 0.0, 1.0)  # clamp and reflect v
        
        i = math.floor(u * self.width)
        j = math.floor(v * self.height)
        
        # image textures may be out of bounds
        if i >= self.width:
            i = self.width-1
        if j >= self.height:
            i = self.height-1
            
        color_scale = 1.0 / 255.0
        pixel = self.data[j * self.width + i]
        
        return raytracer.color(color_scale * pixel[0], color_scale * pixel[1], color_scale * pixel[2])
        
            
            
            
        
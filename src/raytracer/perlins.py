# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingTheNextWeek.html#solidtextures

from src.raytracer import raytracer
from src.raytracer import rweekend
import math

# perlin noise texture
class perlin():
    
    def __init__(self):
        self.point_count = 256
        self.ranfloat = []
        for i in range(0, self.point_count):
            self.ranfloat.append(rweekend.random_double())
            
        self.perm_x = self.perlin_generate_perm()
        self.perm_y = self.perlin_generate_perm()
        self.perm_z = self.perlin_generate_perm()
        
    def noise(self, p):
        if not isinstance(p, raytracer.point3):
            raise TypeError()
            
        i = math.floor(4 * p.x) & 255
        j = math.floor(4 * p.y) & 255
        k = math.floor(4 * p.z) & 255
        
        return self.ranfloat[self.perm_x[i] ^ self.perm_y[j] ^ self.perm_z[k]]
    
    def perlin_generate_perm(self):
        p = []
        for i in range(0, self.point_count):
            p.append(i)
            
        return self.permute(p, self.point_count)
    
    def permute(self, p, n):
        for i in range(n-1, 0, -1):
            target = rweekend.random_int(0, i)
            temp = p[i]
            p[i] = p[target]
            p[target] = temp
        return p
# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingTheNextWeek.html#solidtextures

from src.raytracer import raytracer
from src.raytracer import rweekend
import math

# perlin noise texture
class perlin():
    
    def __init__(self):
        self.point_count = 256
        #self.ranfloat = []
        #for i in range(0, self.point_count):
        #    self.ranfloat.append(rweekend.random_double())
        
        self.ranvec = []
        for i in range(0, self.point_count):
            self.ranvec.append(raytracer.unit(raytracer.vec3.random(-1, 1)))
            
        self.perm_x = self.perlin_generate_perm()
        self.perm_y = self.perlin_generate_perm()
        self.perm_z = self.perlin_generate_perm()
        
    def noise(self, p):
        if not isinstance(p, raytracer.point3):
            raise TypeError()
            
        u = p.x - math.floor(p.x)
        v = p.y - math.floor(p.y)
        w = p.z - math.floor(p.z)
        
        #u = u*u*(3-2*u)
        #v = v*v*(3-2*v)
        #w = w*w*(3-2*w)
        
        i = math.floor(p.x)
        j = math.floor(p.y)
        k = math.floor(p.z)
        c = [[[[], []], [[], []]],
             [[[], []], [[], []]]]
        
        for di in (0, 1):
            for dj in (0, 1):
                for dk in (0, 1):
                    c[di][dj][dk] = self.ranvec[
                        self.perm_x[(i + di) & 255]
                        ^ self.perm_y[(j + dj) & 255]
                        ^ self.perm_z[(k + dk) & 255]]
        #print('c', c)
        return self.trilinear_interp(c, u, v, w)
    
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
    
    def trilinear_interp(self, c, u, v, w):
        uu = u*u*(3-2*u)
        vv = v*v*(3-2*v)
        ww = w*w*(3-2*w)
        accum = 0.0
        for i in (0, 1):
            for j in (0, 1):
                for k in (0, 1):
                    weight_v = raytracer.vec3(u-i, v-j, w-k)
                    accum += (
                        (i * uu + (1-i)*(1-uu))
                        * (j * vv + (1-j) * (1-vv))
                        * (k * ww + (1-k) * (1-ww))
                        * raytracer.dot(c[i][j][k], weight_v)
                    )
        
        return accum
    
    def turb(self, p, depth=7):
        accum = 0.0
        temp_p = p
        weight = 1.0
        
        for i in range(0, depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p *= 2
            
        return abs(accum)
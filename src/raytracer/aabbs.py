# implement ray using example from Peter Shirley
# https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class/vec3utilityfunctions

from src.raytracer import raytracer

# aabb class
# uses args a and b to create a bounding box
class aabb():
    def __init__(self, a=None, b=None):
        # check args are valid
        if isinstance(a, raytracer.point3) or a is None:
            self.minimum = a
        else:
            raise TypeError()
        if isinstance(b, raytracer.point3) or b is None:
            self.maximum = b
        else:
            raise TypeError()
            
    # determine if bounding box is hit
    def hit(self, r, t_min, t_max):
        for a in range(0, 3):
            t0 = min((self.minimum[a] - r.origin[a]) / r.direction[a],
                    (self.maximum[a] - r.origin[a]) / r.direction[a])
            t1 = max((self.minimum[a] - r.origin[a]) / r.direction[a],
                    (self.maximum[a] - r.origin[a]) / r.direction[a])
            t_min = max(t0, t_min)
            t_max = min(t1, t_max)
            if t_max <- t_min:
                return False
        return True

def surrounding_box(box0, box1):
    if not isinstance(box0, aabb):
        raise TypeError()
    if not isinstance(box1, aabb):
        raise TypeError()

    # find minimum point between boxes
    small = raytracer.point3(
        min(box0.minimum.x, box1.minimum.x),
        min(box0.minimum.y, box1.minimum.y),
        min(box0.minimum.z, box1.minimum.z))
    
    big = raytracer.point3(
        min(box0.maximum.x, box1.maximum.x),
        min(box0.maximum.y, box1.maximum.y),
        min(box0.maximum.z, box1.maximum.z))

    return aabb(small, big)
    
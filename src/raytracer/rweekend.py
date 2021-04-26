import random

infinity = float("inf")
pi = 3.1415926535897932385

def degrees_to_radians(degrees):
    return degrees * pi / 180.0

def random_double(seed=None, r_min=None, r_max=None):
    random.seed(seed, version=2)
    if r_min is None or r_max is None:
        return random.random()
    else:
        return random.uniform(r_min, r_max)

def clamp(x, c_min, c_max):
    if isinstance(x, float) and isinstance(c_min, float) and isinstance(c_max, float):
        if x < c_min:
            return c_min
        elif x > c_max:
            return c_max
        else:
            return x
    else:
        raise TypeError()
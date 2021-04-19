# test_raytracer_vec3_class.py

import pytest
from src.raytracer import ray
from src.raytracer import raytracer

def test_ray_empty_init():
    myray = ray.ray()
    assert myray.origin == None
    assert myray.direction == None

def test_ray_init():
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    assert myray.origin == mypt
    assert myray.direction == myvec

def test_ray_at():
    mypt = raytracer.point3(0, 0, 0)
    myvec = raytracer.vec3(2, 2, 0)
    myray = ray.ray(mypt, myvec)
    assert myray.at(0.5) == raytracer.point3(1, 1, 0)

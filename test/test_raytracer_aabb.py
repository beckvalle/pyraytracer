# test_raytracer_vec3_class.py

import pytest
from src.raytracer import aabbs
from src.raytracer import raytracer

def test_aabb_empty_init():
    myaabb = aabbs.aabb()

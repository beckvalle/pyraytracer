# test hittable

import pytest
from src.raytracer import raytracer
from src.raytracer import hittables, materials
from src.raytracer import ray
from dataclasses import dataclass

def test_bvh_init():
    objects = hittables.hittable_list()
    material = materials.lambertian(raytracer.color(0.8, 0.8, 0.0))
    objects.add(hittables.sphere(raytracer.point3(0.0, 0.0, -1.0), 0.5, material))
    objects.add(hittables.sphere(raytracer.point3(-1.0, 0.0, -1.0), 0.5, material))
    objects.add(hittables.sphere(raytracer.point3(-1.0, 0.0, -1.0), -0.4, material))
    objects.add(hittables.sphere(raytracer.point3(1.0, 0.0, -1.0), 0.5, material))
    
    world = hittables.hittable_list()
    world.add(hittables.bvh_node(hlist=objects, _time0=0.0, _time1=1.0))
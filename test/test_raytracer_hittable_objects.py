# test hittable

import pytest
from src.raytracer import raytracer
from src.raytracer import hittables
from src.raytracer import ray
from dataclasses import dataclass

def test_hit_record_base_bad_init():
    with pytest.raises(TypeError):
        myhr = hittables.hit_record("", "", "")

def test_hit_record_base_init():
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), 3.5)
    assert myhr.p == raytracer.point3(1, 2, 3)
    assert myhr.normal == raytracer.point3(4, 5, 6)
    assert myhr.t == 3.5

def test_hittable_init():
    with pytest.raises(TypeError):
        myht = hittables.hittable()

# test ABC = https://clamytoe.github.io/articles/2020/Mar/12/testing-abcs-with-abstract-methods-with-pytest/
def test_hittable_hit():
    hittables.hittable.__abstractmethods__ = set()
    
    @dataclass
    class dummy(hittables.hittable):
        pass
    myd = dummy()
    mypt = raytracer.point3(0, 0, 0)
    myvec = raytracer.vec3(2, 2, 0)
    myd.hit(ray.ray(mypt, myvec), 2.4, 3.4, hittables.hit_record(mypt, myvec, 2.0))
            
def test_sphere_init_values():
    mysph = hittables.sphere(raytracer.point3(1, 2, 3), 3.4)
    assert isinstance(mysph, hittables.sphere)
    assert mysph.center == raytracer.point3(1, 2, 3)
    assert mysph.radius == 3.4

def test_sphere_init_empty():
    mysph = hittables.sphere()
    assert mysph.center == None
    assert mysph.radius == None

def test_sphere_init_bad_values_center():
    with pytest.raises(TypeError):
        mysph = hittables.sphere(3.4, 3.4)

def test_sphere_init_bad_values_radius():
    with pytest.raises(TypeError):
        mysph = hittables.sphere(raytracer.point3(1, 2, 3), "a")

def test_sphere_hit_none_radius_center():
    mysph = hittables.sphere()
    with pytest.raises(AttributeError):
        mysph.hit("", "", "", "")

def test_sphere_hit_bad_ray():
    mysph = hittables.sphere(raytracer.point3(1, 1, 1), 3.0)
    with pytest.raises(TypeError):
        mysph.hit("", "", "", "")

def test_sphere_hit_bad_t_min():
    mysph = hittables.sphere(raytracer.point3(1, 1, 1), 3.0)
    mypt = raytracer.point3(0, 0, 0)
    myvec = raytracer.vec3(2, 2, 0)
    with pytest.raises(TypeError):
        mysph.hit(ray.ray(mypt, myvec), "", "", "")

def test_sphere_hit_bad_t_max():
    mysph = hittables.sphere(raytracer.point3(1, 1, 1), 3.0)
    mypt = raytracer.point3(0, 0, 0)
    myvec = raytracer.vec3(2, 2, 0)
    with pytest.raises(TypeError):
        mysph.hit(ray.ray(mypt, myvec), 2.4, "", "")

def test_sphere_hit_bad_t_rec():
    mysph = hittables.sphere(raytracer.point3(1, 1, 1), 3.0)
    mypt = raytracer.point3(0, 0, 0)
    myvec = raytracer.vec3(2, 2, 0)
    with pytest.raises(TypeError):
        mysph.hit(ray.ray(mypt, myvec), 2.4, 3.4, "")

def test_sphere_hit_bad_ray_vals():
    mysph = hittables.sphere(raytracer.point3(1, 1, 1), 3.0)
    with pytest.raises(AttributeError):
        mysph.hit(ray.ray(), "", "", "")
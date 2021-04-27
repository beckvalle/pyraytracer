# test materials

import pytest
from src.raytracer import raytracer
from src.raytracer import materials
from src.raytracer import hittables
from dataclasses import dataclass
from src.raytracer import ray

def test_material_init():
    with pytest.raises(TypeError):
        myht = materials.material()

# test ABC = https://clamytoe.github.io/articles/2020/Mar/12/testing-abcs-with-abstract-methods-with-pytest/
def test_material_scatter():
    materials.material.__abstractmethods__ = set()
    
    @dataclass
    class dummy(materials.material):
        pass
    myd = dummy()
    myd.scatter("", "", "", "")

def test_lambertian_init():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.lambertian(mycol)

def test_lambertian_bad_init():
    with pytest.raises(TypeError):
        mymat = materials.lambertian("")
        
def test_lambertian_bad_scatter_r_in():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.lambertian(mycol)
    with pytest.raises(TypeError):
        mymat.scatter("", "", "", "")

def test_lambertian_bad_scatter_rec():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.lambertian(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    with pytest.raises(TypeError):
        mymat.scatter(myray, "", "", "")

def test_lambertian_bad_scatter_attenuation():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.lambertian(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    with pytest.raises(TypeError):
        mymat.scatter(myray, myhr, "", "")

def test_lambertian_bad_scatter_scattered():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.lambertian(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    with pytest.raises(TypeError):
        mymat.scatter(myray, myhr, mycol, "")

def test_lambertian_good_scatter():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.lambertian(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    mymat.scatter(myray, myhr, mycol, myray)

def test_lambertian_good_scatter_near_norm():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.lambertian(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    mymat.scatter(myray, myhr, mycol, myray, 3)

def test_metal_init():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.metal(mycol)

def test_metal_bad_init():
    with pytest.raises(TypeError):
        mymat = materials.metal("")
        
def test_metal_bad_scatter_r_in():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.metal(mycol)
    with pytest.raises(TypeError):
        mymat.scatter("", "", "", "")

def test_metal_bad_scatter_rec():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.metal(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    with pytest.raises(TypeError):
        mymat.scatter(myray, "", "", "")

def test_metal_bad_scatter_attenuation():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.metal(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    with pytest.raises(TypeError):
        mymat.scatter(myray, myhr, "", "")

def test_metal_bad_scatter_scattered():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.metal(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    with pytest.raises(TypeError):
        mymat.scatter(myray, myhr, mycol, "")

def test_metal_good_scatter():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.metal(mycol)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    mymat.scatter(myray, myhr, mycol, myray)

def test_dielectric_init():
    mymat = materials.dielectric(0.2)

def test_dielectric_bad_init():
    with pytest.raises(TypeError):
        mymat = materials.dielectric("")
        
def test_dielectric_bad_scatter_r_in():
    mymat = materials.dielectric(0.2)
    with pytest.raises(TypeError):
        mymat.scatter("", "", "", "")

def test_dielectric_bad_scatter_rec():
    mymat = materials.dielectric(0.2)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    with pytest.raises(TypeError):
        mymat.scatter(myray, "", "", "")

def test_dielectric_bad_scatter_attenuation():
    mymat = materials.dielectric(0.2)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    with pytest.raises(TypeError):
        mymat.scatter(myray, myhr, "", "")

def test_dielectric_bad_scatter_scattered():
    mycol = raytracer.color(3, 4, 5)
    mymat = materials.dielectric(0.2)
    mypt = raytracer.point3(3, 4, 5)
    myvec = raytracer.vec3(6, 7, 7)
    myray = ray.ray(mypt, myvec)
    myhr = hittables.hit_record(raytracer.point3(1, 2, 3), raytracer.vec3(4, 5, 6), None, 3.5)
    with pytest.raises(TypeError):
        mymat.scatter(myray, myhr, mycol, "")

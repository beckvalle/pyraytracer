# test_raytracer_vec3_class.py

import pytest
from src.raytracer import raytracer
from math import sqrt
import random


def test_vec3_empty_init():
    myvec = raytracer.vec3()
    assert myvec.x == 0
    assert myvec.y == 0
    assert myvec.z == 0

def test_vec3_full_init():
    myvec = raytracer.vec3(1, 2, 3)
    assert myvec.x == 1
    assert myvec.y == 2
    assert myvec.z == 3

def test_vec3_1val_init():
    myvec = raytracer.vec3(1)
    assert myvec.x == 1
    assert myvec.y == 1
    assert myvec.z == 1

def test_vec3_str():
    myvec = raytracer.vec3()
    assert str(myvec) == '(0, 0, 0)'
    myvec = raytracer.vec3(1, 2, 3)
    assert str(myvec) == '(1, 2, 3)'

def test_vec3_xyz_index():
    myvec = raytracer.vec3(1, 2, 3)
    assert myvec.x == 1
    assert myvec.y == 2
    assert myvec.z == 3
    with pytest.raises(AttributeError):
        myvec.m

def test_vec3_index():
    myvec = raytracer.vec3(1, 2, 3)
    assert myvec[1] == 2

def test_vec3_eq_true():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec2 = raytracer.vec3(1, 2, 3)
    assert myvec1.y == myvec2.y
    assert myvec1 == myvec2

def test_vec3_eq_raw():
    myvec1 = raytracer.vec3(1, 2, 3)
    assert myvec1 == raytracer.vec3(1, 2, 3)

def test_vec3_eq_false():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec2 = raytracer.vec3(4, 5, 6)
    with pytest.raises(AssertionError):
        assert myvec1.y == myvec2.y
    with pytest.raises(AssertionError):
        assert myvec1 == myvec2

def test_vec3_not_eq_true():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec2 = raytracer.vec3(4, 5, 6)
    assert myvec1.y != myvec2.y
    assert myvec1 != myvec2

def test_vec3_not_eq_false():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec2 = raytracer.vec3(1, 2, 3)
    with pytest.raises(AssertionError):
        assert myvec1.y != myvec2.y
    with pytest.raises(AssertionError):
        assert myvec1 != myvec2

def test_vec3_make_neg():
    negvec = -raytracer.vec3(1, 2, 3)
    assert negvec.x == -1
    assert negvec.y == -2
    assert negvec.z == -3

def test_vec3_copy():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec2 = raytracer.vec3(myvec1)
    assert myvec1.y == myvec2.y
    assert myvec1 == myvec2
    
def test_vec3_plus():
    myvec1 = raytracer.vec3(1, 2, 3) + raytracer.vec3(4, 5, 6)
    assert myvec1 == raytracer.vec3(5, 7, 9)

def test_vec3_bad_plus():
    myvec1 = raytracer.vec3(1, 2, 3)
    with pytest.raises(TypeError):
        myvec4 = myvec1 + 3

def test_vec3_plus_eq():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec1 += raytracer.vec3(4, 5, 6)
    assert myvec1 == raytracer.vec3(5, 7, 9)
    
def test_vec3_minus():
    myvec1 = raytracer.vec3(5, 7, 9) - raytracer.vec3(4, 5, 6)
    assert myvec1 == raytracer.vec3(1, 2, 3)

def test_vec3_bad_minus():
    myvec1 = raytracer.vec3(1, 2, 3)
    with pytest.raises(TypeError):
        myvec4 = myvec1 - 3
        
def test_vec3_minus_eq():
    myvec1 = raytracer.vec3(5, 7, 9)
    myvec1 -= raytracer.vec3(4, 5, 6)
    assert myvec1 == raytracer.vec3(1, 2, 3)

def test_vec3_mult_scal():
    myvec1 = raytracer.vec3(1, 2, 3)
    assert myvec1 * 3 == raytracer.vec3(3, 6, 9)

def test_vec3_rmult_scal():
    myvec1 = raytracer.vec3(1, 2, 3)
    assert 3 * myvec1 == raytracer.vec3(3, 6, 9)

def test_vec3_mult_eq_scal():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec1 *= 3
    assert myvec1 == raytracer.vec3(3, 6, 9)
    
def test_vec3_mult_el_vec3():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec2 = raytracer.vec3(4, 5, 6)
    assert myvec1 * myvec2 == raytracer.vec3(4, 10, 18)

def test_vec3_div_scal():
    myvec1 = raytracer.vec3(3, 6, 9)
    assert myvec1 / 3 == raytracer.vec3(1, 2, 3)

def test_vec3_div_eq_scal():
    myvec1 = raytracer.vec3(3, 6, 9)
    myvec1 /= 3
    assert myvec1 == raytracer.vec3(1, 2, 3)

def test_vec3_div_bad_scal():
    myvec1 = raytracer.vec3(1, 2, 3)
    with pytest.raises(ZeroDivisionError):
        myvec1 / 0
        
def test_vec3_len_squared():
    myvec1 = raytracer.vec3(3, 4, 5)
    assert myvec1.len_sqr == 50
    
def test_vec3_len():
    myvec1 = raytracer.vec3(3, 4, 5)
    assert myvec1.len == sqrt(50)

def test_vec3_dot():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec2 = raytracer.vec3(4, 5, 6)
    assert raytracer.dot(myvec1, myvec2) == 32

def test_vec3_bad_dot():
    myvec1 = raytracer.vec3(1, 2, 3)
    with pytest.raises(TypeError):
        raytracer.dot(myvec1, 4)

def test_vec3_cross():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec2 = raytracer.vec3(4, 5, 6)
    assert raytracer.cross(myvec1, myvec2) == raytracer.vec3(-3, 6, -3)

def test_vec3_bad_cross():
    myvec1 = raytracer.vec3(1, 2, 3)
    with pytest.raises(TypeError):
        raytracer.cross(myvec1, 3)

def test_vec3_unit():
    myvec1 = raytracer.vec3(1, 1, 1)
    assert raytracer.unit(myvec1) == raytracer.vec3(1/sqrt(3), 1/sqrt(3), 1/sqrt(3))

def test_vec3_bad_unit():
    with pytest.raises(TypeError):
        raytracer.unit(3)

def test_point3_is_vec3():
    mypt = raytracer.point3(3, 4, 5)
    assert isinstance(mypt, raytracer.vec3)
    assert mypt.y == 4

def test_color_is_vec3():
    mypt = raytracer.color(3, 4, 5)
    assert isinstance(mypt, raytracer.color)
    assert mypt.y == 4

def test_vec3_random():
    myvec1 = raytracer.vec3(0.23796462709189137, 0.23796462709189137, 0.23796462709189137)
    assert str(myvec1) == str(raytracer.vec3.random(seed=3))
    
def test_vec3_random_min_max():
    myvec1 = raytracer.vec3(2.7138938812756743, 2.7138938812756743, 2.7138938812756743)
    assert str(myvec1) == str(raytracer.vec3.random(2.0, 5.0, 3))

def test_random_in_unit_sphere():
    myvec1 = raytracer.vec3(-0.5240707458162173, -0.5240707458162173, -0.5240707458162173)
    assert str(myvec1) == str(raytracer.random_in_unit_sphere(3))

def test_random_in_unit_sphere_ctu():
    myvec1 = raytracer.vec3(0.24580338977940386, 0.24580338977940386, 0.24580338977940386)
    assert str(myvec1) == str(raytracer.random_in_unit_sphere(5))

def test_random_in_hemi_sphere():
    my_norm = raytracer.vec3(1, 2, 3)
    myvec1 = raytracer.vec3(0.5240707458162173, 0.5240707458162173, 0.5240707458162173)
    assert str(myvec1) == str(raytracer.random_in_hemisphere(my_norm, 3))

def test_random_in_hemi_sphere_neg():
    my_norm = raytracer.vec3(-1, -2, -3)
    myvec1 = raytracer.vec3(-0.5240707458162173, -0.5240707458162173, -0.5240707458162173)
    assert str(myvec1) == str(raytracer.random_in_hemisphere(my_norm, 3))

def test_random_in_hemi_sphere_bad_nrom():
    myvec1 = raytracer.vec3(0.5240707458162173, 0.5240707458162173, 0.5240707458162173)
    with pytest.raises(TypeError):
        myvec1 = raytracer.random_in_hemisphere("", 3)

def test_vec3_near_zero_v1():
    myvec = raytracer.vec3(0, 0, 0)
    assert myvec.near_zero() == True

def test_vec3_near_zero_v2():
    myvec = raytracer.vec3(0, 0, 1)
    assert myvec.near_zero() == False
    
def test_vec3_near_zero_v3():
    myvec = raytracer.vec3(0, 0, 0.000000000000001)
    assert myvec.near_zero() == True    
# test_raytracer_vec3_class.py

import pytest
from src.raytracer import raytracer
from math import sqrt


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
    
def test_vec3_mult():
    myvec1 = raytracer.vec3(1, 2, 3)
    assert myvec1 * 3 == raytracer.vec3(3, 6, 9)

def test_vec3_mult_eq():
    myvec1 = raytracer.vec3(1, 2, 3)
    myvec1 *= 3
    assert myvec1 == raytracer.vec3(3, 6, 9)   

def test_vec3_div():
    myvec1 = raytracer.vec3(3, 6, 9)
    assert myvec1 / 3 == raytracer.vec3(1, 2, 3)

def test_vec3_div_eq():
    myvec1 = raytracer.vec3(3, 6, 9)
    myvec1 /= 3
    assert myvec1 == raytracer.vec3(1, 2, 3)

def test_vec3_div_bad():
    myvec1 = raytracer.vec3(1, 2, 3)
    with pytest.raises(ZeroDivisionError):
        myvec1 / 0
        
def test_vec3_len_squared():
    myvec1 = raytracer.vec3(3, 4, 5)
    assert myvec1.len_sqr == 50
    
def test_vec3_len():
    myvec1 = raytracer.vec3(3, 4, 5)
    assert myvec1.len == sqrt(50)
    
def test_point3_is_vec3():
    mypt = raytracer.point3(3, 4, 5)
    assert isinstance(mypt, raytracer.vec3)
    assert mypt.y == 4

def test_color_is_vec3():
    mypt = raytracer.color(3, 4, 5)
    assert isinstance(mypt, raytracer.color)
    assert mypt.y == 4
    
    
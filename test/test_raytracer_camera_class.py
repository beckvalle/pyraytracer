# test_raytracer_vec3_class.py

import pytest
from src.raytracer import camera
from src.raytracer import raytracer
from src.raytracer import ray

def test_camera_empty_init():
    aspect_ratio = 16.0 / 9.0
    viewport_height = 2.0
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1.0
    origin = raytracer.point3(0, 0, 0)
    horizontal = raytracer.vec3(viewport_width, 0.0, 0.0)
    vertical = raytracer.vec3(0.0, viewport_height, 0.0)
    lower_left_corner = origin - horizontal / 2 - vertical / 2 - raytracer.vec3(0, 0, focal_length)

    mycamera = camera.camera()
    assert mycamera.aspect_ratio == aspect_ratio
    assert mycamera.viewport_height == viewport_height
    assert mycamera.viewport_width == viewport_width
    assert mycamera.focal_length == focal_length
    assert mycamera.origin == origin
    assert mycamera.horizontal == horizontal
    assert mycamera.vertical == vertical
    assert mycamera.lower_left_corner == lower_left_corner

def test_camera_get_ray_empty():
    mycamera = camera.camera()
    with pytest.raises(TypeError):
        mycamera.get_ray()

def test_camera_get_ray_bad_u():
    mycamera = camera.camera()
    with pytest.raises(TypeError):
        mycamera.get_ray("", "")

def test_camera_get_ray_bad_v():
    mycamera = camera.camera()
    with pytest.raises(TypeError):
        mycamera.get_ray(2.0, "")

def test_camera_get_ray():
    mycamera = camera.camera()
    myray = mycamera.get_ray(2.0, 3.6)
    assert isinstance(myray, ray.ray)
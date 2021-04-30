# test hittable

import pytest
from src.raytracer import raytracer
from src.raytracer import textures
from dataclasses import dataclass

def test_texture_init():
    textures.texture.__abstractmethods__ = set()
    
    @dataclass
    class dummy(textures.texture):
        pass
    
    myd = dummy()
    myd.value("", "", "")
    
def test_image_texture_init():
    mytext = textures.image_texture()
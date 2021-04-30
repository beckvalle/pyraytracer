# test hittable

import pytest
from src.raytracer import raytracer
from src.raytracer import perlins
from dataclasses import dataclass

def test_perlin_init():
    perlins.perlin()
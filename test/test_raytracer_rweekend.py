# test hittable

import pytest
from src.raytracer import rweekend

def test_rweekend_values():
    assert rweekend.infinity == float("inf")
    assert rweekend.pi == 3.1415926535897932385

def test_deg_to_rad():
    assert rweekend.degrees_to_radians(90) == 1.5707963267948966
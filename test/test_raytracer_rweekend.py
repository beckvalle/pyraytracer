# test hittable

import pytest
from src.raytracer import rweekend

def test_rweekend_values():
    assert rweekend.infinity == float("inf")
    assert rweekend.pi == 3.1415926535897932385

def test_deg_to_rad():
    assert rweekend.degrees_to_radians(90) == 1.5707963267948966

def test_clamp_bad_x():
    with pytest.raises(TypeError):
        rweekend.clamp("", "", "")

def test_clamp_bad_min():
    with pytest.raises(TypeError):
        rweekend.clamp(2.0, "", "")

def test_clamp_bad_max():
    with pytest.raises(TypeError):
        rweekend.clamp(2.0, 2.4, "")

def test_clamp_x_less_min():
    x = rweekend.clamp(1.0, 3.0, 5.0)
    assert x == 3.0

def test_clamp_x_greater_max():
    x = rweekend.clamp(7.0, 3.0, 5.0)
    assert x == 5.0

def test_clamp_x_between_min_max():
    x = rweekend.clamp(5.0, 3.0, 7.0)
    assert x == 5.0
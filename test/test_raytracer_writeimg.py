# test_raytracer_writeimg.py

import pytest
import warnings
from src.raytracer import raytracer
from src.raytracer import writeimg

def test_writeppm_empty():
    myvec = writeimg.writeppm()
    assert myvec.image_width == None
    assert myvec.image_height == None
    assert myvec.col_code == 'P3'
    assert myvec.max_col == 255
    assert myvec.out_file == 'outfile.ppm'
    assert myvec.color_string == ''

def test_writeppm():
    myvec = writeimg.writeppm(256, 257, 'outfile.ppm', 'P4', 233)
    assert myvec.image_width == 256
    assert myvec.image_height == 257
    assert myvec.col_code == 'P4'
    assert myvec.max_col == 233
    assert myvec.out_file == 'outfile.ppm'

def test_writeppm_write_head(tmpdir):
    file = tmpdir.join('test_outppm.ppm')
    myvec = writeimg.writeppm(256, 257, file.strpath, 'P3', 255)
    myvec.write_head()
    assert file.read() == 'P3\n256 257\n255\n'

def test_writeppm_write_color_string():
    myvec = writeimg.writeppm()
    assert myvec.color_string == ''
    myvec.write_color(raytracer.vec3(0.75, 0.5, 0.5))
    myvec.write_color(raytracer.vec3(0.5, 0.5, 0.5))
    assert myvec.color_string == "191 127 127\n127 127 127\n"
    
def test_writeppm_write_color_file(tmpdir):
    file = tmpdir.join('test_outppm.ppm')
    myvec = writeimg.writeppm(256, 257, file.strpath, 'P3', 255)
    myvec.write_color(raytracer.vec3(0.75, 0.5, 0.5))
    myvec.write_color(raytracer.vec3(0.5, 0.5, 0.5))
    myvec.write_head()
    myvec.write_color_file()
    assert file.read() == 'P3\n256 257\n255\n191 127 127\n127 127 127\n\n'

def test_writeppm_write_bad_color_file(tmpdir):
    file = tmpdir.join('test_outppm.ppm')
    myvec = writeimg.writeppm(256, 257, file.strpath, 'P3', 255)
    with pytest.raises(writeimg.NoHeaderError):
        myvec.write_color_file()

def test_writeppm_write_empty_color_string(tmpdir):
    file = tmpdir.join('test_outppm.ppm')
    myvec = writeimg.writeppm(256, 257, file.strpath, 'P3', 255)
    myvec.write_head()
    with pytest.warns(UserWarning):
        myvec.write_color_file()

def test_writeppm_check_valid(tmpdir):
    file = tmpdir.join('test_outppm.ppm')
    myvec = writeimg.writeppm(1, 2, file.strpath, 'P3', 255)
    myvec.write_color(raytracer.vec3(0.75, 0.5, 0.5))
    myvec.write_color(raytracer.vec3(0.5, 0.5, 0.5))
    assert myvec.check_valid()[0] == True
    
def test_writeppm_bad_check_valid(tmpdir):
    file = tmpdir.join('test_outppm.ppm')
    myvec = writeimg.writeppm(1, 3, file.strpath, 'P3', 255)
    myvec.write_color(raytracer.vec3(0.75, 0.5, 0.5))
    myvec.write_color(raytracer.vec3(0.5, 0.5, 0.5))
    assert myvec.check_valid()[0] == False
    
def test_writeppm_bad_none_check_valid(tmpdir):
    myvec = writeimg.writeppm()
    assert myvec.check_valid()[0] == False
    
def test_writeppm_bad_no_str_check_valid(tmpdir):
    file = tmpdir.join('test_outppm.ppm')
    myvec = writeimg.writeppm(1, 3, file.strpath, 'P3', 255)
    assert myvec.check_valid()[0] == False

def test_writeppm_write_color_string_per_px():
    myvec = writeimg.writeppm()
    myvec.write_color(raytracer.vec3(0.75, 0.5, 0.5), 3)
    assert myvec.color_string == "63 42 42\n"
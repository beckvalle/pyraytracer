# write PPM file

import warnings
import math
from src.raytracer.raytracer import vec3

class NoHeaderError(Exception):
    pass

class writeppm():

    def __init__(self, image_width=None, image_height=None, out_file='outfile.ppm', col_code='P3', max_col=255):
        self.image_width = image_width  # image columns
        self.image_height = image_height  # image rows
        self.col_code = col_code  # P3 means the colors are ASCII
        self.max_col = max_col  # 225 is max color value
        self.out_file = out_file  # output file name
        self.color_string = ''
        self.header_written = False

    def write_head(self):
        with open(self.out_file, 'w') as outf:
            outf.write(str(self.col_code)+"\n")
            outf.write(str(self.image_width)+" "+str(self.image_height)+"\n")
            outf.write(str(self.max_col)+"\n")
        self.header_written = True

    def write_color_file(self):
        if self.header_written:
            if self.color_string is not '':
                with open(self.out_file, 'a') as outf:
                    outf.write(str(self.color_string)+"\n")
            else:
                warnings.warn("Color string is empty", UserWarning)
        else:
            raise NoHeaderError("File header must be written before color values added")

    def write_color(self, pixel_color):
        self.color_string += (str(math.floor(255.999 * pixel_color.x)) + " "
                              + str(math.floor(255.999 * pixel_color.y)) + " "
                              + str(math.floor(255.999 * pixel_color.z)) + "\n")

    def check_valid(self):
        if self.image_width is not None and self.image_height is not None and self.color_string is not None:
            if self.image_width * self.image_height == len(self.color_string.rstrip().split("\n")):
                return [True, 'params OK']
            else:
                return [False, str(self.image_width * self.image_height)+" != "+str(len(self.color_string.rstrip().split("\n")))]
        else:
            return [False, "value is None"]
        
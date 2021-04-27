# write PPM file

import warnings
import math
from src.raytracer.raytracer import vec3
from src.raytracer import rweekend

# create custom error to check if header has been written
class NoHeaderError(Exception):
    pass

# this class saves image metadata, checks for validity, and writes
# header and pixel colors to a ppm file
class writeppm():

    def __init__(self, image_width=None, image_height=None, out_file='outfile.ppm', col_code='P3', max_col=255):
        self.image_width = image_width  # image columns
        self.image_height = image_height  # image rows
        self.col_code = col_code  # P3 means the colors are ASCII
        self.max_col = max_col  # 225 is max color value
        self.out_file = out_file  # output file name
        self.color_string = ''
        self.header_written = False

    # write image file header
    def write_head(self):
        with open(self.out_file, 'w') as outf:
            outf.write(str(self.col_code)+"\n")
            outf.write(str(self.image_width)+" "+str(self.image_height)+"\n")
            outf.write(str(self.max_col)+"\n")
        self.header_written = True

    # write image pixel values from color string
    def write_color_file(self):
        if self.header_written:
            if self.color_string is not '':
                with open(self.out_file, 'a') as outf:
                    outf.write(str(self.color_string)+"\n")
            else:
                warnings.warn("Color string is empty", UserWarning)
        else:
            raise NoHeaderError("File header must be written before color values added")

    def write_color(self, pixel_color, samples_per_pixel=1):
        # set RGB to pixel values
        r = pixel_color.x
        g = pixel_color.y
        b = pixel_color.z

        # divide color by number of samples and gamma correct for gamma 2.0
        scale = 1.0 / samples_per_pixel
        r = math.sqrt(scale * r)
        g = math.sqrt(scale * g)
        b = math.sqrt(scale * b)
        
        # translate color values to a string
        self.color_string += (str(math.floor(255.999 * rweekend.clamp(r, 0.0, 0.999))) + " "
                              + str(math.floor(255.999 * rweekend.clamp(g, 0.0, 0.999))) + " "
                              + str(math.floor(255.999 * rweekend.clamp(b, 0.0, 0.999))) + "\n")

    def check_valid(self):
        
        # check image object has a width, height, and color string
        if self.image_width is not None and self.image_height is not None and self.color_string is not None:
            if self.image_width * self.image_height == len(self.color_string.rstrip().split("\n")):
                return [True, 'params OK']
            else:
                return [False, str(self.image_width * self.image_height)+" != "+str(len(self.color_string.rstrip().split("\n")))]
        else:
            return [False, "value is None"]
        
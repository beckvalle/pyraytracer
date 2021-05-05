import sys
import math

from src.raytracer.raytracer import point3, vec3, color, unit
from src.raytracer.raytracer import unit, dot
from src.raytracer.raytracer import random_in_hemisphere, random_unit_vector
from src.raytracer.ray import ray
from src.raytracer import hittables, materials, textures
from src.raytracer import camera, writeimg, rweekend
from datetime import datetime
import pytz

# used to get a color for a ray with a background color
def ray_color(r, background, world, depth):
    rec = hittables.hit_record()
    if depth <= 0:
        return color(0, 0, 0)
    
    # if ray hits nothing return background color
    hit_out = world.hit(r, 0.001, rweekend.infinity, rec)
    if not hit_out[0]:
        return background
    
    if hit_out[0]:
        rec = hit_out[1]
        
        scattered = ray()
        attenuation = vec3()
        #print("rec: ", rec, "\n")
        emitted = rec.material.emitted(rec.u, rec.v, rec.p)
        #print("emit: ", emitted, '\n')
            
        out = rec.material.scatter(r, rec, attenuation, scattered)
        #print("out: ", out, '\n')
        if out[0]:
            scattered = out[1]
            attenuation = out[2]
            return (emitted + attenuation * ray_color(scattered, background, world, depth-1))
        return emitted
    
# setup code for scene with a bunch of random spheres
def random_scene():
    world = hittables.hittable_list()
    
    ground_material = materials.lambertian(color(0.5, 0.5, 0.5))
    world.add(hittables.sphere(point3(0.0, -1000, 0.0), 1000.0, ground_material))
    
    for a in range(-2, 2):
        for b in range(-2, 2):
            choose_mat = rweekend.random_double()
            center = point3(a + 0.9 * rweekend.random_double(), 0.2, b + 0.9 * rweekend.random_double())
            
            if ((center - point3(4.0, 0.2, 0.0)).len > 0.9):
                if (choose_mat < 0.8):
                    # diffuse sphere
                    albedo = color.random() * color.random()
                    sphere_material = materials.lambertian(albedo)
                    center2 = center + vec3(0.0, rweekend.random_double(0.0, 0.5), 0.0) # add moving sphere
                    world.add(hittables.moving_sphere(center, center2, 0.0, 1.0, 0.2, sphere_material))
                elif (choose_mat < 0.95):
                    # metal sphere
                    albedo = color.random(0.5, 1.0)
                    fuzz = rweekend.random_double(0.0, 0.5)
                    sphere_material = materials.metal(albedo, fuzz)
                    world.add(hittables.sphere(center, 0.2, sphere_material))
                else:
                    # glass sphere
                    sphere_material = materials.dielectric(1.5)
                    world.add(hittables.sphere(center, 0.2, sphere_material))

    material1 = materials.dielectric(1.5)
    world.add(hittables.sphere(point3(0.0, 1.0, 0.0), 1.0, material1))
    
    material2 = materials.lambertian(color(0.4, 0.2, 0.1))
    world.add(hittables.sphere(point3(-4.0, 1.0, 0.0), 1.0, material2))
    
    material3 = materials.metal(color(0.7, 0.6, 0.5), 0.0)
    world.add(hittables.sphere(point3(4.0, 1.0, 0.0), 1.0, material3))
    
    return world

# scene setup for two large spheres
def two_spheres():
    objects = hittables.hittable_list()
    
    checker = textures.checker_texture(color(0.2, 0.3, 0.1), color(0.9, 0.9, 0.9))
    objects.add(hittables.sphere(point3(0.0, -10, 0.0), 10.0, materials.lambertian(checker)))
    objects.add(hittables.sphere(point3(0.0, 10, 0.0), 10.0, materials.lambertian(checker)))
    
    return objects
    
def two_perlin_spheres():
    objects = hittables.hittable_list()
    
    perlin_text_basic = textures.noise_texture(4.0)
    objects.add(hittables.sphere(point3(0.0, -1000.0, 0.0), 1000.0, materials.lambertian(perlin_text_basic)))
    objects.add(hittables.sphere(point3(0.0, 2.0, 0.0), 2.0, materials.lambertian(perlin_text_basic)))
    
    return objects

def earth():
    earth_texture = textures.image_texture("earthmap.jpg")
    earth_surface = materials.lambertian(earth_texture)
    globe = hittables.sphere(point3(0.0, 0.0, 0.0), 2.0, earth_surface)
    
    return hittables.hittable_list(globe)

def simple_light():
    objects = hittables.hittable_list()
    
    perlin_text_basic = textures.noise_texture()
    objects.add(hittables.sphere(point3(0.0, -1000.0, 0.0), 1000.0, materials.lambertian(perlin_text_basic)))
    objects.add(hittables.sphere(point3(0.0, 2.0, 0.0), 2.0, materials.lambertian(perlin_text_basic)))
    
    difflight = materials.diffuse_light(color(4, 4, 4))
    objects.add(hittables.xy_rect(3.0, 5.0, 1.0, 3.0, -2.0, difflight))
    
    return objects

def simple_light_2():
    objects = hittables.hittable_list()
    
    red = materials.lambertian(color(0.65, 0.05, 0.05))
    green = materials.lambertian(color(0.12, 0.45, 0.15))
    white = materials.lambertian(color(0.73, 0.73, 0.73))
    
    main_box = hittables.box(point3(-1.0, 0.0, -3.0), point3(-0.5, 4.0, -4.0), red)
    objects.add(main_box)
    box_trans = hittables.translate(main_box, vec3(1.0, 0.0, 0.0))
    objects.add(box_trans)
    box_trans = hittables.translate(box_trans, vec3(1.0, 0.0, 0.0))
    objects.add(box_trans)
    
    base_sphere = hittables.sphere(point3(-3.0, 1.0, 1.0), 1.0, white)
    objects.add(base_sphere)
    sphere_shift = hittables.translate(base_sphere, vec3(3.0, 0.0, 0.0))
    sphere_shift = hittables.recolor(sphere_shift, red)
    objects.add(sphere_shift)
    sphere_shift = hittables.translate(sphere_shift, vec3(3.0, 0.0, 0.0))
    sphere_shift = hittables.recolor(sphere_shift, green)
    objects.add(sphere_shift)
    
    objects.add(hittables.xz_rect(-50.0, 50.0, -50.0, 50.0, 0.0, green))
    #objects.add(hittables.xy_rect(-12.0, -12.0, -1.0, 2.0, -15.0, white))
    
    difflight = materials.diffuse_light(color(6, 6, 6))
    objects.add(hittables.sphere(point3(6.0, 8.0, 6.0), 5.0, difflight))
    
    return objects

# choose scene
scene_number = 3

# scene defaults
vfov = 40.0
aperture = 0.0
background = color(0,0,0)
aspect_ratio = 16.0 / 9.0

# scene vars per scene

# random small spheres and 3 big ones
if scene_number == 1:
    world = random_scene()
    background = color(0.70, 0.80, 1.00)
    lookfrom = point3(13, 2, 3)
    lookat = point3(0, 0, 0)
    vfov = 20.0
    aperture = 0.1
    
# 2 large checker spheres
elif scene_number == 2:
    world = two_spheres()
    background = color(0.70, 0.80, 1.00)
    lookfrom = point3(13, 2, 3)
    lookat = point3(0, 0, 0)
    vfov = 20.0
    
# 1 small and 1 large perlin sphere
elif scene_number == 3:
    world = two_perlin_spheres()
    background = color(0.70, 0.80, 1.00)
    lookfrom = point3(13, 2, 3)
    lookat = point3(0, 0, 0)
    vfov = 20.0
    
# show globe
elif scene_number == 4:
    world = earth()
    background = color(0.70, 0.80, 1.00)
    lookfrom = point3(13, 2, 3)
    lookat = point3(0, 0, 0)
    vfov = 20.0
    
elif scene_number == 5:
    world = earth()
    background = color(0.0, 0.0, 0.0)
    lookfrom = point3(13, 2, 3)
    lookat = point3(0, 0, 0)
    vfov = 20.0
    
elif scene_number == 6:
    world = simple_light()
    # samples_per_pixel = 40;
    background = color(0.0, 0.0, 0.0)
    lookfrom = point3(26.0, 3.0, 6.0)
    lookat = point3(0, 2, 0)
    vfov = 20.0

elif scene_number == 7:
    world = simple_light_2()
    background = color(0.0, 0.0, 0.0)
    lookfrom = point3(0.0, 3.0, 20.0)
    lookat = point3(0, 2, 0)
    vfov = 20.0
    
# common camera params
vup = vec3(0,1,0)
dist_to_focus = 10.0
cam = camera.camera(lookfrom, lookat, vup, 20.0, aspect_ratio, 
                    aperture, dist_to_focus, 0.0, 1.0)

# image params
image_width = 200
image_height = math.floor(image_width / aspect_ratio)
samples_per_pixel = 7 
max_depth = 20
# 50/20 8 min

# print start time
tz_CH = pytz.timezone('America/Chicago') 
start_time = datetime.now(tz_CH)
print("start time: ", start_time.strftime("%H:%M:%S"))

# render image
outimg = writeimg.writeppm(image_width, image_height,
                           'outfile.ppm', 'P3', 255)
outimg.write_head()
for j in range(image_height-1, -1, -1):
    sys.stdout.write("\r%d%%" % j)
    sys.stdout.flush()
    for i in range(0, image_width):
        pixel_color = color(0, 0, 0)
        for s in range(0, samples_per_pixel):
            u = float(i + rweekend.random_double())/(image_width - 1)
            v = float(j + rweekend.random_double())/(image_height - 1)
            r = cam.get_ray(u, v)
            pixel_color += ray_color(r, background, world, max_depth)
            #print("pixel_color", pixel_color)
        outimg.write_color(pixel_color, samples_per_pixel)
sys.stdout.write("done")

# check if valid file vars
outimg.check_valid()

# write ppm file
outimg.write_color_file()

# print start time
end_time = datetime.now(tz_CH)
elpsd_time = end_time-start_time
print("end time: ", end_time.strftime("%H:%M:%S"))
print("elapsed time: ", elpsd_time)
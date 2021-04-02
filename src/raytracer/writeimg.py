# write PPM file

image_width = 256;  # output image width
image_height = 256;  # output image height

with open("render.ppm", "w") as f:  # open the file for writing
    f.write("P3\n")  # colors are ASCII
    # add comments into file
    f.write("# P3 means the colors are ASCII\n")  
    f.write("# "+str(image_width)+" "+str(image_height)+" indicates columns and rows\n")
    f.write("# 225 is max color\n")
    f.write("# after is RGB triplets\n")
    # file parameters
    f.write(str(image_width)+" "+str(image_height)+"\n")
    f.write("255\n")
    # add data
    for j in range(image_height-1, -1, -1):
        print("scanlines remaining:"+str(j), end="\r")  # indicate progress
        for i in range(0, image_width):
            r = float(i)/(image_width-1)
            g = float(j)/(image_height-1)
            b = 0.25

            ir = str(int(255.999 * r))
            ig = str(int(255.999 * g))
            ib = str(int(255.999 * b))
    
            f.write(ir+" "+ig+" "+ib+"\n")

    f.close()
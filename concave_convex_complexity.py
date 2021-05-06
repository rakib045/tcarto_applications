import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from skimage.transform import PiecewiseAffineTransform, warp
from skimage import data
from PIL import Image, ImageDraw
from colormap import rgb2hex
from collections import Counter
from sympy.geometry import *


input_img_file = "input/test1.png"

output_img_filename = "output/out_test1_180_180_convex.png"
last_point_position = [180, 180]

output_img_filename = "output/out_test1_80_80_concave.png"
last_point_position = [80, 80]





image = Image.open(input_img_file)
image = image.convert("RGBA")

output_image_size = image.size

x2 = Point(0, 0)
x3 = Point(output_image_size[0], 0)
x1 = Point(0, output_image_size[1])
x4 = Point(output_image_size[0], output_image_size[1])
x_4 = Point(last_point_position[0], last_point_position[1])

init_area = Polygon(x1, x2, x3, x4).area
mod_area = Polygon(x1, x2, x3, x_4).area
perc_area = float(mod_area/init_area)

print("Init Area:" + str(init_area))
print("Modified Area:" + str(mod_area))
print("Current Area Percentage:" + str(perc_area))

rows, cols = output_image_size[0], output_image_size[1]

src_cols = np.linspace(0, cols, 2)
src_rows = np.linspace(0, rows, 2)
src_rows, src_cols = np.meshgrid(src_rows, src_cols)
src = np.dstack([src_cols.flat, src_rows.flat])[0]

dst_cols = np.linspace(0, cols, 2)
dst_rows = np.linspace(0, rows, 2)
dst_rows, dst_cols = np.meshgrid(dst_rows, dst_cols)
dst = np.dstack([dst_cols.flat, dst_rows.flat])[0]

src[3] = last_point_position

tform = PiecewiseAffineTransform()
tform.estimate(src, dst)

out_rows = output_image_size[0]
out_cols = output_image_size[1]
out = warp(image, tform, output_shape=(out_rows, out_cols))
plt.imsave(output_img_filename, out)

occurence_count = Counter(image.getdata())

red_count = 0
black_count = 0
total_count = 0
for occ in occurence_count:
    total_count += occurence_count[occ]
    if occ[3] < 100:
        continue
    if occ[0] > 100 and (occ[1] == occ[2]):
        if occ[0] != occ[1]:
            red_count += occurence_count[occ]

    if occ[0] == occ[1] == occ[2]:
        if occ[0] < 100:
            black_count += occurence_count[occ]

print("Input Image : total = " + str(total_count))
print("Input Image : red = " + str(red_count))
print("Input Image : black = " + str(black_count))


image = Image.open(output_img_filename)
image = image.convert("RGBA")

occurence_count = Counter(image.getdata())

red_count = 0
black_count = 0
total_count = 0
for occ in occurence_count:
    total_count += occurence_count[occ]
    if occ[3] < 100:
        continue
    if occ[0] > 100 and (occ[1] == occ[2]):
        if occ[0] != occ[1]:
            red_count += occurence_count[occ]

    if occ[0] == occ[1] == occ[2]:
        if occ[0] < 100:

            black_count += occurence_count[occ]

print("Output Image : total = " + str(total_count))
print("Output Image : red = " + str(red_count))
print("Output Image : black = " + str(black_count))


print("Red should be = " + str(red_count*perc_area))
print("Black should be = " + str(black_count*perc_area))

b_error = (black_count*perc_area - black_count) / (black_count*perc_area)
r_error = (red_count*perc_area - red_count) / (red_count*perc_area)
print("Red Error = " + str(r_error))
print("Black Error = " + str(b_error))
from PIL import Image, ImageDraw
import sys
import os
import random

LENS = 50

DEFAULT_WIDTH = 4
DEFAULT_HEIGHT = 6

if len(sys.argv) != 4:
	sys.exit("Add the images as arguments and resolution!")

image1 = sys.argv[1]
image2 = sys.argv[2]
res = int(sys.argv[3])

mask_size = (res/LENS)
print("Mask size:" + str(mask_size))

## make own procedure --
#Calculate pixel size depenending on inputted resolution
im_width = res*DEFAULT_WIDTH
im_height = res*DEFAULT_HEIGHT
pixel_size = (im_width, im_height)
print(pixel_size)

im1 = Image.open(image1)
im1 = im1.resize(pixel_size)

im2 = Image.open(image2)
im2 = im2.resize(pixel_size)
## -- end


## Make first image transparent??
#(using https://stackoverflow.com/questions/765736/how-to-use-pil-to-make-all-white-pixels-transparent)

# COME BACK: Could try pattern??
# im1 = im1.convert("RGBA") #Adds opacity
# pixel_data1 = im1.load()
#
#
# for b in range(im_height):
# 	for a in range(im_width):
# 		if pixel_data1[a, b] == (255, 255, 255, 255):
# 			pixel_data1[a, b] = (255, 255, 255, 0)

### --- Attempt to make a pattern, similar to Photoshop
half_mask = int(mask_size/2)
alpha_pattern = Image.new("RGBA", (int(mask_size), int(mask_size)), (255, 255, 255, 0))
draw = ImageDraw.Draw(alpha_pattern)
#Here rectangle has to subtract 0.5 to find true middle pixel
draw.rectangle( ((0, 0), (int(half_mask-0.5),int(mask_size)) ), fill=(0,0,0,255))
#alpha_pattern.show()

# Make a correctly size (4x6) image with the transparency layers

overall_pattern = Image.new("RGBA", (int(im_width), int(im_height)), (255, 255, 255, 0))

#Need to iterate in batches
# helpful: https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks

def batch(iterable, n=1):
	l = len(iterable)
	for num in range(0,l,n):
		yield iterable[num:min(num + n, l)]

range_width = list(range(0,im_width))
range_height = list(range(0, im_height))

for b in batch(range_width, int(mask_size)):
	for a in batch(range_height, int(mask_size)):
		overall_pattern.paste(alpha_pattern, (a[0],b[0]))
### --- end

## use alpha composite here for im1, 2,
im3 = Image.composite(im1, im2, overall_pattern)
#im3.show()

im3 = im3.save("final_interlace.jpg", dpi=(res,res))

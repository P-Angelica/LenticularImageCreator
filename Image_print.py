from PIL import Image, ImageDraw
import sys
import os
import random
import math

LENS = 50
NUM_OF_LENT = 200;

DEFAULT_WIDTH = 4
DEFAULT_HEIGHT = 6
DEFAULT_RATIO = float(2/3)
SIXTH = float(1/6)

NUM_OF_IMG = 3 ## Should become variable

## Ensure round to nearest multiple
#(https://datagy.io/python-round-to-multiple/)
def round_to_multiple(number, multiple):
	return multiple *round(number/multiple)

## Calculate area for proper 4x6 crop of original image
## Assumes the height is larger than width
def calculate_croparea(image):
	image_width, image_height = image.size
	fixed_width = image_height * DEFAULT_RATIO
	difference_width = (image_width - fixed_width)/2
	area = (math.floor(difference_width), 0, math.floor(fixed_width+difference_width), image_height)
	return area

### -- Entry Information
###
if len(sys.argv) != 5:
	sys.exit("Add the two images as arguments and an image resolution!")
image1 = sys.argv[1]
image2 = sys.argv[2]
image3 = sys.argv[3]
## Here we should ensure that the resolution is divisible by LPI 50
res = int(sys.argv[4])
if not(res%LENS == 0):
	sys.exit(f"Please enter an image resolution that is divisible by {LENS}")
###
### -- end


### -- To create the alpha pattern, we need to know how many pixels for lens
###
# Ex. A resolution of 300 dpi(dots per inch) for 50 lpi(lens per inch)
# Pixels available under 1 lenticle = 300/50 = 6 image pixels under 1
PIX_PER_LENT = math.floor(res/LENS)
print("Lenticle image size:" + str(PIX_PER_LENT))

## Number of pixels of 1 image per lenticle
# Ex. If above (300/50) is 6 pixels per lenticle,
## then a 3-image interlacing equals a 2-pixel column for each image (2*3 = 6)
PIX_PER_COLUMN = PIX_PER_LENT / NUM_OF_IMG

# Procedure for calculating the FULL pixel size depending on inputted resolution
# If the inputted resolution was 300 for a 4x6in photo
# Resolution must at MIN be at 1200 x 1800 ppi (pixels per inch)
im_width = res*DEFAULT_WIDTH
im_height = res*DEFAULT_HEIGHT
pixel_size = (im_width, im_height)
print(pixel_size)

## Transforms the image into a scaled version of original 4x6 crop
im1 = Image.open(image1)
area1 = calculate_croparea(im1)
im1 = im1.crop(area1)
im1 = im1.resize((im_width, im_height),Image.Resampling.LANCZOS)

im2 = Image.open(image2)
area2 = calculate_croparea(im2)
im2 = im2.crop(area2)
im2 = im2.resize((im_width, im_height),Image.Resampling.LANCZOS)


im3 = Image.open(image3)
area3 = calculate_croparea(im3)
im3 = im3.crop(area3)
im3 = im3.resize((im_width, im_height),Image.Resampling.LANCZOS)
###
### -- end

## ---- New algorithm

### --- Make a new correctly size (4x6) image with a transparency layer, ex. 1200x1800 mask of transparent 6 pixel stripes
overall_pattern = Image.new("RGBA", (int(im_width), int(im_height)), (255, 255, 255, 255))

### ---- Make a rectangular mask for pasting image strips ----
mask_rectangle = Image.new("L", overall_pattern.size, 0)
draw_rect = ImageDraw.Draw(mask_rectangle)
shifting_Lborder = 0;
shifting_Rborder = 0;
#draw_rect.rectangle((shifting_Lborder,0, shifting_Rborder, im_height), fill=255)
#mask_rectangle.save("mask_rectangle.jpg", quality=100)
#mask_rectangle.show()

#overall_pattern.show()
print("Width of Image:", im_width, end="\n")
print("Number of Lenticles:", NUM_OF_LENT, end="\n")
print("Pixels Per Column:", PIX_PER_COLUMN, end="\n")
old_pix = 0



for i in range(0, im_width):
	shifting_Rborder = i
	column_of_pixel = (i // PIX_PER_COLUMN)

	selection_image = old_pix % NUM_OF_IMG
	if selection_image == 0:
		color_r = 255
	elif selection_image == 1:
		color_r = 0
	elif selection_image == 2:
		color_r = 127

	if old_pix != column_of_pixel:
		#print("O(p):"+str(old_pix))
		#print("First XY:",shifting_Lborder,0, "SECOND XY:",shifting_Rborder, im_height)
		draw_rect.rectangle((shifting_Lborder, 0, shifting_Rborder, im_height), fill=color_r)
		shifting_Lborder = i;
		mask_rectangle.save("mask_rectangle.jpg", quality=100)

	old_pix = column_of_pixel
	images_from_pixel = (column_of_pixel % NUM_OF_LENT)
	#print(i, images_from_pixel)

mask_rectangle.show()

# overall_pattern.paste(im1, (0,0), mask_rectangle)
# overall_pattern.save("test_mask.jpg+, quality=100)

# PRE - 4/9

# ## Need to iterate through pixels in batches, ex. 0 -> 6, 6 -> 12
# ## Taken from: https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks
# def batch(iterable, n=1):
# 	l = len(iterable)
# 	for num in range(0,l,n):
# 		yield iterable[num:min(num + n, l)]
#
# range_width = list(range(0,im_width))
# range_height = list(range(0, im_height))
#
#
# #Skip every batch of list items, take the first list item
# for a in batch(range_width, int(PIX_PER_LENT)):
# 	print(a[0],0, a[0]+PIX_PER_COLUMN, im_height)
# 	#overall_pattern.paste([NEW IMAGE HERE], (a[0],im_height))
#
# ###
# ### --- end
#
#
# for y in range(NUM_OF_IMG+1):
# 		print((math.floor(x/PIX_PER_COLUMN)%200))
# # 	# run through pixel columns until a complete set of 1
# # 	# crop the column set and set it on white image
# # 	# repeat until done
# # #do next image







# #//OLD CODE below
#
#
# ### --- Similar to photoshop, make a pattern of pixels for interlacing
# ###
# # here make the 2-image split, if 6 pixel mask then 3 pixels per image
# half_mask = int(PIX_PER_LENT/2)
#
# # create the transparent mask (0-value at the end), ex. 6 pixels
# alpha_pattern = Image.new("RGBA", (int(PIX_PER_LENT), int(PIX_PER_LENT)), (255, 255, 255, 0))
# draw = ImageDraw.Draw(alpha_pattern)
# #Here rectangle for centering the split subtracts 0.5 to find true "middle" pixel
# draw.rectangle( ((0, 0), (int(half_mask-0.5),int(PIX_PER_LENT)) ), fill=(0,0,0,255))
# #alpha_pattern.show()
#
# ### --- Make a new correctly size (4x6) image with a transparency layer, ex. 1200x1800 mask of transparent 6 pixel stripes
# ###
# overall_pattern = Image.new("RGBA", (int(im_width), int(im_height)), (255, 255, 255, 0))
#
# ## Need to iterate through pixels in batches, ex. 0 -> 6, 6 -> 12
# ## Taken from: https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks
# def batch(iterable, n=1):
# 	l = len(iterable)
# 	for num in range(0,l,n):
# 		yield iterable[num:min(num + n, l)]
#
# range_width = list(range(0,im_width))
# range_height = list(range(0, im_height))
#
# #Skip every batch of list items, take the first list item drop a masked pixel until complete
# for b in batch(range_height, int(PIX_PER_LENT)):
# 	for a in batch(range_width, int(PIX_PER_LENT)):
# 		#print(a[0], b[0])
# 		overall_pattern.paste(alpha_pattern, (a[0],b[0]))
# #overall_pattern.show()
# ###
# ### --- end
#
# ### --- Create final image with both images + the mask
# ###
# ## use alpha composite here for im1, 2,
# print(im1.size)
# print(im2.size)
# im3 = Image.composite(im1, im2, overall_pattern)
# #im3.show()
#
# #Save the final image into system folder at the specified resolution from the start
# im3 = im3.save("final_interlace.jpg", dpi=(res,res))
# # ###
# # ### -- end

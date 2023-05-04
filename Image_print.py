from PIL import Image, ImageDraw
import sys
import os
import random
import math


### VARIABLES ###
##

LENS = 49.6
NUM_OF_LENT = 200;

DEFAULT_WIDTH = 4
DEFAULT_HEIGHT = 6
DEFAULT_RATIO = float(2/3)

MAX_IMG_NUM = 11;

NUM_OF_IMG = 0;
images = {}

##################################
##################################

### FUNCTIONS ###
##

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

## Select image to extract pixel column
def select_image(count):
	column_of_pixel = (count // PIX_PER_COLUMN) # C(P) = floor( p / a )= count / 2
	selection_image = column_of_pixel % NUM_OF_IMG #S(c(p)) = c(p) % 3
	print("image"+str(int(selection_image)+1))
	selection_image = images["image"+str(int(selection_image)+1)]
	return selection_image

#######################################################################################################
#######################################################################################################

### -- Input Information -- ###
###
if (len(sys.argv) < 5) or (len(sys.argv) > MAX_IMG_NUM+3):
	sys.exit(f"Please input between 2 to {MAX_IMG_NUM} images as argument, a printer resolution, and a lenticular size!\n"
			 "Input format should be: [image name] [image name] ... [printer resolution][lens per inch]")

# Determining how many images were provided to interlace, variable
# original count includes the .py file, so subtract 1
input_len = len(sys.argv) - 1
# Subtract the res number and LPI attached at the end
NUM_OF_IMG = input_len - 2

# Assign a dictionary item to input image
for x in range(1, (NUM_OF_IMG+1)):
	images["image{0}".format(x)] = sys.argv[x]

## Here we should ensure that the resolution is divisible by provided LPI
res = int(sys.argv[input_len-1])
LENS = int(sys.argv[input_len])
# if not(res%LENS == 0):
# 	sys.exit(f"Please enter an image resolution that is divisible by {LENS}")

#######################################################################################################
#######################################################################################################

## TESTING VARIABLE INPUTS

### --

# Ex. A resolution of 300 dpi(dots per inch) for 50 lpi(lens per inch)
# Pixels available under 1 lenticle = 300/50 = 6 image pixels under 1
""" COME BACK HERE ASAP """
PIX_PER_LENT = res/LENS
#PIX_PER_LENT = math.floor(res/LENS)
print(PIX_PER_LENT)
#print("Lenticle image size:" + str(PIX_PER_LENT))

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

## Transforms the image into a scaled version of original 4x6 crop, variable
for key in images:
	edit_im = Image.open(images[key])
	area = calculate_croparea(edit_im)
	edit_im = edit_im.crop(area)
	edit_im = edit_im.resize((im_width, im_height),Image.Resampling.LANCZOS)
	images[key] = edit_im

###
### -- end

## ---- New algorithm

### --- Make a new correctly size (4x6) image with a transparency layer, ex. 1200x1800 mask of transparent 6 pixel stripes
overall_pattern = Image.new("RGB", (int(im_width), int(im_height)), (255, 255, 255, 255))

### ---- Make shifting border variables for crop ----
shifting_Lborder = 0;
shifting_Rborder = 0;

print("Width of Image:", im_width, end="\n")
# print("Number of Lenticles:", NUM_OF_LENT, end="\n")
print("Pixels Per Column:", PIX_PER_COLUMN, end="\n")

## Count through image resolution width and assign an input image
for i in range(0, im_width):

	## Run algorithm to select input image for final image ###
	selection_image = select_image(i)

	## Crop a column of the selected image and paste onto final image
	selection_image = selection_image.crop((i, 0, i+1, im_height))
	overall_pattern.paste(selection_image,(i, 0, i+1, im_height))

## Save final version
overall_pattern.save("final_interlace.jpg", dpi=(res,res))

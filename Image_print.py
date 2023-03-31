from PIL import Image, ImageDraw
import sys
import os
import random
import math

LENS = 50
DEFAULT_WIDTH = 4
DEFAULT_HEIGHT = 6
DEFAULT_RATIO = float(2/3)
SIXTH = float(1/6)


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
if len(sys.argv) != 4:
	sys.exit("Add the two images as arguments and an image resolution!")

image1 = sys.argv[1]
image2 = sys.argv[2]
res = int(sys.argv[3])
### -- end


### -- To create the alpha pattern, we need to know how many pixels for lens
###
# Ex. A resolution of 300 dpi(dots per inch) for 50 lpi(lens per inch)
# Mask = 300/50 = 6 image pixels under 1 lens, for 2-image split that's 3 pixels per image
mask_size = math.floor(res/LENS)
	#decimal.Decimal(res/LENS).quantize(decimal.Decimal('0.00'), rounding=decimal.ROUND_HALF_EVEN)
#print("Mask size:" + str(mask_size))

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
###
### -- end

#//uncomment below


### --- Similar to photoshop, make a pattern of pixels for interlacing
###
# here make the 2-image split, if 6 pixel mask then 3 pixels per image
half_mask = int(mask_size/2)

# create the transparent mask (0-value at the end), ex. 6 pixels
alpha_pattern = Image.new("RGBA", (int(mask_size), int(mask_size)), (255, 255, 255, 0))
draw = ImageDraw.Draw(alpha_pattern)
#Here rectangle for centering the split subtracts 0.5 to find true "middle" pixel
draw.rectangle( ((0, 0), (int(half_mask-0.5),int(mask_size)) ), fill=(0,0,0,255))
#alpha_pattern.show()

### --- Make a new correctly size (4x6) image with a transparency layer, ex. 1200x1800 mask of transparent 6 pixel stripes
###
overall_pattern = Image.new("RGBA", (int(im_width), int(im_height)), (255, 255, 255, 0))

## Need to iterate through pixels in batches, ex. 0 -> 6, 6 -> 12
## Taken from: https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks
def batch(iterable, n=1):
	l = len(iterable)
	for num in range(0,l,n):
		yield iterable[num:min(num + n, l)]

range_width = list(range(0,im_width))
range_height = list(range(0, im_height))

#Skip every batch of list items, take the first list item drop a masked pixel until complete
for b in batch(range_height, int(mask_size)):
	for a in batch(range_width, int(mask_size)):
		#print(a[0], b[0])
		overall_pattern.paste(alpha_pattern, (a[0],b[0]))
#overall_pattern.show()
###
### --- end

### --- Create final image with both images + the mask
###
## use alpha composite here for im1, 2,
print(im1.size)
print(im2.size)
im3 = Image.composite(im1, im2, overall_pattern)
#im3.show()

#Save the final image into system folder at the specified resolution from the start
im3 = im3.save("final_interlace.jpg", dpi=(res,res))
# ###
# ### -- end

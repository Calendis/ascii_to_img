# Python script to turn ASCII into an image
# ASCII is base 256, so we can store 3*n*n characters in an n*n image
# (That's n*n characters on each of the R, G, and B channels)
# Bert Myroon
# 14 Nov., 2019

from sys import argv
from PIL import Image
from itertools import chain
import os.path

MAX_PIXELS = 100000000
OUTPUT_FILE_NAME = "message_image"

def main():
	arguments = argv
	# Make sure we have exactly three given arguments, for a total of four
	if len(arguments) != 4:
		print_usage("length")
		return

	# Make sure the size arguments are valid
	try:
		arguments[1] = int(arguments[1])
		arguments[2] = int(arguments[2])
		assert(arguments[1] > 0)
		assert(arguments[2] > 0)
		assert(arguments[1] * arguments[2] <= MAX_PIXELS)
	except:
		print_usage("number")
		return

	# Make sure the file exists
	if not os.path.isfile(arguments[3]):
		print_usage("notfile")
		return
	else:
		# File exists
		message = open(arguments[3]).read()

	# Make sure the message contains only ASCII characters
	for char in message:
		if ord(char) > 255:
			print_usage("character")
			print("Invalid character:", char)
			return

	# Make sure the image is long enough to contain the message
	try:
		assert(len(message)-1 <= 3*arguments[1]*arguments[2])
	except:
		print_usage("toolong", len(message), arguments[1], arguments[2])
		return

	# Error checking passed
	width = arguments[1]
	height = arguments[2]
	print("Your message length is", len(message)-1)
	print("Your image can contain a maximum message length of", 3*width*height)
	print("Converting text to image...")
	
	# Convert message to ASCII
	encoded_message = [ord(char) for char in message]

	# Fill the end of the message (up to the max message length for this image size) with null bytes
	encoded_message += [0 for x in range(3*width*height - len(message))]
	
	# Set up a list of lists which represents the image
	rgb_image = []
	for ix in range(height):
		rgb_image.append([])
	for row in rgb_image:
		for iy in range(width):
			row.append([0, 0, 0])

	# Populate the image list with RGB values
	# The message is written along the red channel, and wraps around to the blue channel, and then the green
	# I use the formula (val_count*width*height)+rgb_count+(row_count*width) to calculate all three values at once
	# so I don't have to actually make three passes
	index = -1
	row_count = -1
	for row in rgb_image:
		row_count += 1
		rgb_count = -1
		#print("ROW", row_count, ":", row)
		for rgb in row:
			rgb_count += 1
			val_count = -1
			for val in rgb:
				val_count += 1
				index += 1
				
				# This format writes the R, G, and B channels simultaneously
				# it is more likely to leave blank rows at the end of the image
				'''rgb[val_count] = encoded_message[index]'''
				
				# This format writes R first, then loops back around to G, and then B
				# It can only leave a blank row if the message length is < 1/3 of the image area
				rgb[val_count] = encoded_message[(val_count*width*height)+rgb_count+(row_count*width)]

	#print("AFTER RGB IMAGE:", rgb_image, "\n")

	# Format for use in PIL and output
	# The chain flattens the list by one dimension
	print("Formatting data...")
	flattened_rgb_image = list(chain(*rgb_image))
	flattened_rgb_image = [tuple(l) for l in flattened_rgb_image]
	message_image = Image.new("RGB", (width, height), 255)
	print("Saving file...")
	message_image.putdata(flattened_rgb_image)
	message_image.save(OUTPUT_FILE_NAME+".png")
	print("All done")


def print_usage(error_type, longlength=0, w=0, h=0):
	
	if error_type == "length":
		print("Invalid number of arguments.")
		print("Please provide an image width and length, followed by a path to a text file.")

	elif error_type == "number":
		print("Invalid image size arguments.")
		print("Please provide two positive integers which multiply to a maximum of", MAX_PIXELS)

	elif error_type == "notfile":
		print("The provided file does not exist.")

	elif error_type == "character":
		print("Invalid characters in file.")
		print("Your message may only contain ASCII charaters.")

	elif error_type == "toolong":
		print("Message of length " + str(longlength) + " is too long for given image size.")
		print("The maximum length of the message is the image width multiplied by the image height multiplied by 3.")
		print("The maximum amount of characters that can be contained in the given image size is", 3*w*h)

	else:
		print("Unspecified error. This should not occur!")

main()
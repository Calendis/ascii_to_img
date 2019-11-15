# Python script to turn images from my ASCII to image script back into text
# Bert Myroon
# 14 Nov., 2019

from sys import argv
import os.path
from PIL import Image

def main():
	arguments = argv
	# Make sure we have one given argument, for a total of two
	if len(arguments) != 2:
		print_usage("no of arguments")
		return

	# Make sure the file exists
	if not os.path.isfile(arguments[1]):
		print_usage("does not exist")
		return

	# Error checking passed
	image = Image.open(arguments[1])
	pixels = image.load()

	width = image.size[0]
	height = image.size[0]

	red_characters = []
	green_characters = []
	blue_characters = []

	for ix in range(width):
		for iy in range(height):
			try:
				red_characters.append(pixels[iy, ix][0])
			except:
				pass
			try:
				green_characters.append(pixels[iy, ix][1])
			except:
				pass
			try:
				blue_characters.append(pixels[iy, ix][2])
			except:
				pass

	# A dumb hack one-liner
	#decoded_message = [(chr(v) if v != 0 else " ") for v in red_characters] + [(chr(v) if v != 0 else " ") for v in green_characters] + [(chr(v) if v != 0 else " ") for v in blue_characters]

	# A better way using three loops
	decoded_message = []
	for v in red_characters:
		decoded_message.append(chr(v))
	for v in green_characters:
		decoded_message.append(chr(v))
	for v in blue_characters:
		decoded_message.append(chr(v))

	# Strip the trailing null bytes from the end.
	# These occur because you probably won't fill an ENTIRE n*m image with text while encoding,
	# so decoding picks up a bunch of black at the end (null bytes)
	bytes_to_strip = 0
	decoded_message.reverse()
	for i in range(len(decoded_message)):
		if decoded_message[i] == chr(0):
			bytes_to_strip += 1
		else:
			break # We don't want to strip ALL the null bytes, only trailing ones!

	decoded_message.reverse()

	# Remove the bytes marked by the list of bools
	for i in range(bytes_to_strip):
		decoded_message.pop()

	# Output the message. It could be written to a file using '>' in bash
	print(*decoded_message, sep="")


def print_usage(error_type):
	if error_type == "no of arguments":
		print("Invalid arguments.")
		print("Please provide one argument, a path to an image.")

	elif error_type == "does not exist":
		print("Given file does not exist.")

main()
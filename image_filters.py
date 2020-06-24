from PIL import Image
from random import randint, uniform
import numpy as np

class Manga():
	""" This filter restrics an image to black and white, causing images to 
	resemble a black and white comic or manga. """

	def __init__(self, cutoff=128):
		self.cutoff = cutoff

	def set_cuttoff(self):
		self.cutoff = cutoff

	def modify_pixel(self, pixel_value):

		if pixel_value < self.cutoff:
			return 0

		return 255

	def filter_image(self, img):
		return img.convert(mode="L").point(lambda pixel: self.modify_pixel(pixel))


class Inverse():
	""" This filter inverts every pixel of an image. """

	def __init__(self):
		pass

	def modify_pixel(self, pixel_value):
		return 255 - pixel_value

	def filter_image(self, img):
		""" Called by the user on an image. Returns a filtered version
		    of the given image."""
		bands = img.convert(mode="RGB").split()
		new_bands = [None, None, None]

		# Invert each value of each band. Merge resultant bands.
		for i in range(3):
			new_bands[i] = bands[i].point(lambda pixel: self.modify_pixel(pixel))
		
		return Image.merge("RGB", new_bands)
		

class AmplifyBands():
	""" This filter amplifies the RGB bands in an image by a specified factor.
	"""

	def __init__(self, r_factor, g_factor, b_factor):
		self.factors = [r_factor, g_factor, b_factor]

	def modify_pixel(self, pixel_value, factor):
		# Multiply given pixel by factor and return result.
		new_val = pixel_value * factor

		if new_val > 255:
			return 255

		return new_val

	def filter_image(self, img):
		""" Called by the user on an image. Returns a filtered version
		    of the given image."""
		img_bands = img.convert(mode="RGB").split()
		new_bands = [0, 0, 0]

		# Amplify each band by its respective factor.
		for i in range(3):
			new_bands[i] = img_bands[i].point(lambda pixel: self.modify_pixel(pixel, self.factors[i]))

		return Image.merge("RGB", new_bands)


class RestrictColors():
	""" This filter restricts an image's colors to the ones given by the user. 
	    It does this by converting the image to B&W and using the value to 
	    determine what color the pixel should be based on given cutoff values.
	"""

	def __init__(self, colors=[(0, 0, 0), (255, 255, 255)], cutoffs=[128]):

		if len(cutoffs) != len(colors) - 1:
			raise ValuError("Mismatch between number of cutoffs and number of colors.")

		self.colors = colors
		self.cutoffs = cutoffs

	def modify_pixel(self, band, pixel):

		# Set new_val for pixels greater than final cutoff.
		new_val = self.colors[-1][band]

		# Test pixel against all cutoffs. If pixel lower than cutoff, 
		# return value for that cutoff's color.
		for i in range(len(self.cutoffs)):

			if pixel < self.cutoffs[i]:
				new_val = self.colors[i][band]
				break

		return new_val

	def filter_image(self, img):
		""" Called by the user on an image. Returns a filtered version
		    of the given image. """
		new_bands = [None, None, None]
		bw = img.convert(mode="L")

		# Apply filter to BW image 3 times, one for each band. 
		# Merge modified bands.
		for i in range(3):
			new_bands[i] = bw.point(lambda pixel: self.modify_pixel(i, pixel))

		return Image.merge("RGB", new_bands)


class Discombobulate():
	""" This filter applies noise to each pixel randomly. """

	def __init__(self, probability=0.5):
		self.probability = probability

	def set_probability(self, probability):
		self.probability = probability

	def skew_pixel(self, pixel):
		""" Add a random offest to each pixel. """

		if uniform(0, 1) < self.probability:
			offset = randint(-255, 255)

			if pixel + offset > 255:
				return 255

			if pixel + offset < 0:
				return 0

			return pixel + offset

		return pixel

	def filter_image(self, img):
		""" Called by the user on an image. Returns a filtered version
		    of the given image."""
		bands = img.convert(mode="RGB").split()
		new_bands = [None, None, None]

		# Apply filter to each band and merge bands back together.
		for i in range(3):
			new_bands[i] = bands[i].point(lambda pixel: self.skew_pixel(pixel))

		return Image.merge("RGB", new_bands)

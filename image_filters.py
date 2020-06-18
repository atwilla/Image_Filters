from PIL import Image
import numpy as np

class Manga():

	def __init__(self, color1=0, color2=255, cutoff=128):
		self.c1 = color1
		self.c2 = color2
		self.cutoff = cutoff

	def modify_pixel(self, pixel_value):

		if pixel_value < self.cutoff:
			return self.c1

		return self.c2

	def filter_image(self, img):
		return img.convert(mode="L").point(lambda pixel: self.modify_pixel(pixel))


class Inverse():

	def __init__(self):
		pass

	def modify_pixel(self, pixel_value):
		return 255 - pixel_value

	def filter_image(self, img):
		bands = img.convert(mode="RGB").split()
		new_bands = [None, None, None]

		for i in range(3):
			new_bands[i] = bands[i].point(lambda pixel: self.modify_pixel(pixel))
		
		return Image.merge("RGB", new_bands)
		

class AmplifyBands():

	def __init__(self, r_factor, g_factor, b_factor):
		self.factors = [r_factor, g_factor, b_factor]

	def modify_pixel(self, pixel_value, factor):
		new_val = pixel_value * factor

		if new_val > 255:
			return 255

		return new_val

	def filter_image(self, img):
		img_bands = img.convert(mode="RGB").split()
		new_bands = [0, 0, 0]

		for i in range(3):
			new_bands[i] = img_bands[i].point(lambda pixel: self.modify_pixel(pixel, self.factors[i]))

		return Image.merge("RGB", new_bands)
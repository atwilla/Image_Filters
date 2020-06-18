from PIL import Image
import numpy as np
import sys

img = Image.open("ger.png").convert(mode="RGB")
pixels = np.array(list(img.getdata()))
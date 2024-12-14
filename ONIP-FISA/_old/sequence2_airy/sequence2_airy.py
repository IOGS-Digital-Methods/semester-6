import pandas
import numpy as np
import matplotlib.pyplot as plt

# Image avec PIL
from PIL import Image
img = Image.open('airy_1mm.bmp')
img.show()

# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = img.size
print('W='+str(width)+ ' - H='+str(height))


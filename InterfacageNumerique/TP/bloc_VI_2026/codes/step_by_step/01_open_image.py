"""01_open_image.py
Image opening with OpenCV
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>

@see: https://iogs-lense-training.github.io/image-processing/contents/opencv.html#open-an-image
@see: https://iogs-lense-training.github.io/image-processing/contents/opencv.html#display-an-image
"""

import cv2
from matplotlib import pyplot as plt


image_rgb = cv2.imread('./_data/robot.jpg', cv2.IMREAD_UNCHANGED)
image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)

image_gray = cv2.imread('./_data/robot.jpg', cv2.IMREAD_GRAYSCALE)

plt.figure()
plt.imshow(image_rgb)
plt.figure()
plt.imshow(image_gray) #, cmap='gray')
plt.show()


# Information on the images
print(f'Type RGB image: {type(image_rgb)} / Dtype: {image_rgb.dtype}')
print(f'RGB shape: {image_rgb.shape}')
print(f'Gray shape: {image_gray.shape}')

'''
print(f'First Pixel RGB : {image_rgb[0, 0]}')
print(f'First Pixel Gray : {image_gray[0, 0]}')
'''

'''
# Rec. 709
# 0,2126, 0,7152 et 0,0722
Y_lum = 0.2126 * image_rgb[0, 0, 0] + 0.7152 * image_rgb[0, 0, 1] + 0.0722 * image_rgb[0, 0, 2]
print(f'First Pixel Luminance (Rec.709) : {Y_lum}')
'''

# Change space color
'''
image_yuv = cv2.cvtColor(image_rgb , cv2.COLOR_RGB2YUV)
print(f'First Pixel YUV : {image_yuv[0, 0]}')
'''
"""04_threshold.py
Threshold with OpenCV
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>

@see: https://iogs-lense-training.github.io/image-processing/contents/opencv.html#binarize-an-image
"""

import cv2
from matplotlib import pyplot as plt

image_gray = cv2.imread('./_data/robot.jpg', cv2.IMREAD_GRAYSCALE)
max_value = 255
threshold = 100

retval, binary_image = cv2.threshold(image_gray, threshold, max_value, cv2.THRESH_BINARY)

print(f'Retval: {retval}')

# Display images
fig, ax = plt.subplots(nrows=1, ncols=2)
ax[0].imshow(image_gray, cmap='gray')
ax[0].set_title('Initial Gray Image')
ax[1].imshow(binary_image, cmap='gray')
ax[1].set_title('Binary Image')
plt.show()
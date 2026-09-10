import numpy as np  # for numerical operations
from scipy.fft import fft2, ifft2, fftshift  # for Fourier Transform
import matplotlib.pyplot as plt  # for plotting
import cv2

dir_path = './_data/'
ref_path = dir_path+'mire_rep_V2_1.png'
image_ref = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
test_path = dir_path+'mire_tik_V2.png'
image_test = cv2.imread(test_path, cv2.IMREAD_GRAYSCALE)

# Display the reference image
plt.figure()
plt.imshow(image_ref, cmap='gray')
plt.title('Reference Image')
plt.axis('off')

# ALGO ?
result = cv2.matchTemplate(
    image_test,
    image_ref,
    cv2.TM_CCOEFF_NORMED
)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

print("Meilleure corrélation :", max_val)
print("Position :", max_loc)

# CONVOLUTION ?
h, w = image_ref.shape

# Corrélation normalisée
result = cv2.matchTemplate(image_test, image_ref, cv2.TM_CCOEFF_NORMED)

plt.figure()
plt.imshow(result, cmap='gray')
plt.title('Cross Correlation')
plt.axis('off')



# Positions dont le score dépasse le seuil
threshold = 0.95
ys, xs = np.where(result >= threshold)

matches = [(x, y, result[y, x]) for x, y in zip(xs, ys)]

print(matches)

plt.show()

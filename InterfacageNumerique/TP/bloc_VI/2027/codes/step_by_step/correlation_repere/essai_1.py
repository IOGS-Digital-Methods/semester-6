import numpy as np  # for numerical operations
from scipy.fft import fft2, ifft2, fftshift  # for Fourier Transform
import matplotlib.pyplot as plt  # for plotting
import cv2

dir_path = './_data/'
ref_path = dir_path+'mire_rep.png'
image_ref = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
test_path = dir_path+'mire_tik.png'
image_test = cv2.imread(test_path, cv2.IMREAD_GRAYSCALE)

# Display the reference image
plt.figure()
plt.imshow(image_ref, cmap='gray')
plt.title('Reference Image')
plt.axis('off')

# CORRELATION
h, w = image_ref.shape
# Corrélation normalisée
result = cv2.matchTemplate(image_test, image_ref, cv2.TM_CCOEFF_NORMED)

# Affichage de la corrélation
plt.figure()
plt.imshow(result, cmap='gray')
plt.title('Cross Correlation')
plt.axis('off')

# Seuil de corrélation
threshold = 0.9
# Positions dont la valeur est supérieure au seuil
ys, xs = np.where(result >= threshold)

matches = [(x, y, result[y, x]) for x, y in zip(xs, ys)]

## AFFICHAGE
plt.figure()
plt.imshow(image_test, cmap='gray')

for m in matches:
    print(m)
    plt.plot(m[0], m[1], "ro")
    #plt.text(x + 10, y - 10, f"({m['x']}, {m['y']})", color="red")

plt.axis("off")
plt.show()

import cv2
import numpy as np
from matplotlib import pyplot as plt
from form_detection import detect_shape, detect_circles

# Parameters
MIN_AREA = 1
APPROX_FACTOR = 0.02
GAUSS_SIZE = (7, 7)         # Taille du flou gaussien
GAUSS_SIGMA = 1.9

img_gray = cv2.imread('./_data/formes_blanc_30ms.png', cv2.IMREAD_GRAYSCALE)

# Image de sortie (couleur)
img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

## BLUR ?
# Kernel
kernel_size = (21, 21)
# Blur
img_detect = cv2.GaussianBlur(img_gray, kernel_size, 5)

circles = detect_circles(img_detect)

for (x, y, r) in circles:
    cv2.circle(img_out, (x, y), r, (0, 255, 0), 3)
    cv2.putText(img_out, "Cercle", (x - 20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# =========================
#   AFFICHAGE
# =========================
plt.figure()
plt.imshow(img_gray, cmap='gray')
plt.title("Image Initiale")

plt.figure()
plt.imshow(img_out)
plt.title("Formes détectées (polygones + cercles)")

plt.show()

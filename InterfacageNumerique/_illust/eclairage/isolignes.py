import cv2
import matplotlib.pyplot as plt
import numpy as np

# Exemple d'image (2D)
img = cv2.imread('Image_AOI.png', cv2.IMREAD_GRAYSCALE)

# Couleurs type relief
levels = np.linspace(img.min(), img.max(), 20)

img = cv2.GaussianBlur(img, (7,7), 2)

# Zones colorées
plt.contourf(img, levels=levels, cmap="terrain")

# Isolignes
plt.contour(img, levels=levels, colors="black", linewidths=0.5)

plt.colorbar(label="Intensité")
plt.title("Carte d'isolignes (type relief)")
plt.axis("off")
plt.show()

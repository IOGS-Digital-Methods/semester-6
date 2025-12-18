import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('./_data/formes_bruit.png')
zone_vert_rgb = img_rgb[250:350, 700:800, :]
img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
zone_vert_hsv = img_hsv[250:350, 700:800, :]

img_rgb = cv2.imread('./_data/forms_vi.png')
zone_bleu_rgb = img_rgb[430:510, 700:780, :]
img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
zone_bleu_hsv = img_hsv[430:510, 700:780, :]


histogram_v_rgb = cv2.calcHist([zone_bleu_rgb], [2], None, [256], [0, 256])
histogram_v_hsv = cv2.calcHist([zone_bleu_hsv], [0], None, [256], [0, 256])

histogram_b_rgb = cv2.calcHist([zone_bleu_rgb], [2], None, [256], [0, 256])
histogram_b_hsv = cv2.calcHist([zone_bleu_hsv], [0], None, [256], [0, 256])

# =========================
#   AFFICHAGE
# =========================
plt.figure()
plt.imshow(img_rgb)
plt.title("Image Initiale")

plt.figure()
plt.imshow(zone_bleu_rgb)
plt.title("Zone forme bleu")

plt.figure()
plt.plot(histogram_rgb)
plt.plot(histogram_hsv)
plt.title("Histogramme G / Forme verte")
plt.show()

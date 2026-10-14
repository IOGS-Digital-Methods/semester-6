dir_image_path = '../../_data/'
import sys
sys.path.append("../../_libs/")

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

zone_verte = (700, 250, 800, 350) # x0, y0, x1, y1
zone_bleue = (700, 430, 780, 510) # x0, y0, x1, y1

rect_vert = Rectangle(
    (zone_verte[0], zone_verte[1]), zone_verte[2]-zone_verte[0], zone_verte[3]-zone_verte[1],
    fill=False, edgecolor="red", linewidth=2
)
rect_bleu = Rectangle(
    (zone_bleue[0], zone_bleue[1]), zone_bleue[2]-zone_bleue[0], zone_bleue[3]-zone_bleue[1],
    fill=False, edgecolor="red", linewidth=2
)

img_rgb_v = cv2.imread(dir_image_path+'formes_bruit.png')
zone_vert_rgb = img_rgb_v[250:350, 700:800, :]
img_hsv = cv2.cvtColor(img_rgb_v, cv2.COLOR_BGR2HSV)
zone_vert_hsv = img_hsv[250:350, 700:800, :]

img_rgb_b = cv2.imread(dir_image_path+'forms_vi.png')
zone_bleu_rgb = img_rgb_b[430:510, 700:780, :]
img_hsv = cv2.cvtColor(img_rgb_b, cv2.COLOR_BGR2HSV)
zone_bleu_hsv = img_hsv[430:510, 700:780, :]


histogram_v_rgb = cv2.calcHist([zone_vert_rgb], [1], None, [256], [0, 256])
histogram_v_hsv_h = cv2.calcHist([zone_vert_hsv], [0], None, [256], [0, 256])
histogram_v_hsv_s = cv2.calcHist([zone_vert_hsv], [1], None, [256], [0, 256])

histogram_b_rgb = cv2.calcHist([zone_bleu_rgb], [2], None, [256], [0, 256])
histogram_b_hsv_h = cv2.calcHist([zone_bleu_hsv], [0], None, [256], [0, 256])
histogram_b_hsv_s = cv2.calcHist([zone_bleu_hsv], [1], None, [256], [0, 256])

# =========================
#   AFFICHAGE
# =========================
fig, ax = plt.subplots(nrows=2, ncols=3)
ax[0,0].imshow(img_rgb_b)
ax[0,0].add_patch(rect_bleu)

ax[0,0].set_title('Initial RGB Image / Blue')
ax[0,1].imshow(zone_bleu_rgb)
ax[0,1].set_title('Blue zone')
ax[0,2].plot(histogram_b_rgb, label='Blue zone')
ax[0,2].plot(histogram_v_rgb, label='Green zone')
ax[0,2].set_title('RGB - Histogram (normalized)')
ax[1,0].imshow(img_rgb_v)
ax[1,0].add_patch(rect_vert)
ax[1,0].set_title('Initial RGB Image / Green')
ax[1,1].imshow(zone_vert_rgb)
ax[1,1].set_title('Green zone')
ax[1,2].plot(histogram_b_hsv_h, label='Blue zone (H)')
ax[1,2].plot(histogram_v_hsv_h, label='Green zone (H)')
ax[1,2].plot(histogram_b_hsv_s, label='Blue zone (S)')
ax[1,2].plot(histogram_v_hsv_s, label='Green zone (S)')
ax[1,2].legend()
ax[1,2].set_title('HSV - Histogram')
plt.show()

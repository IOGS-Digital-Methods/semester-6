
import cv2
import numpy as np
import sys
sys.path.append("../_libs/")
from form_detection import detect_shape
from images_manipulation import generate_histogram

### Parameters
img_dir_path = '../_data/'
hist_thickness = 3
MIN_AREA = 200          # taille min bruit objet (pas de bruit)
APPROX_FACTOR = 0.02    # tolérance pour la fonction approxPolyDP

### Other functions
def generate_image(image, contours, min_area, approx_factor, title=''):
    for cnt in contours:
        shape, approx, peri = detect_shape(cnt, min_area=min_area, approx_factor=approx_factor)

        # draw
        cv2.drawContours(image, [approx], -1, (255, 0, 0), 2)

        # txt
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(image, shape, (cX - 30, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)



img_gray = cv2.imread(img_dir_path+'formes_blanc_30ms.png', cv2.IMREAD_GRAYSCALE)

### Results list of dictionary - threshold, contours
res_list = []

### Process 1 - No Blur / Bin. OTSU / No min area
title = 'No Blur / Bin. OTSU / No min area / Approx = 0.02'
approx = 0.02
min_area_proc = 1
# Otsu
thresh_value, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Contours
contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
res_dict = {'threshold': thresh_value, 'contours': contours,
            'img_thresh': img_thresh, 'min_area': min_area_proc,
            'approx_factor': approx, 'title': title}
res_list.append(res_dict)

### Process 2 - No Blur / Bin. OTSU / Min area
title = 'No Blur / Bin. OTSU / Min area = 200 / Approx = 0.02'
approx = 0.02
min_area_proc = 200
# Otsu
thresh_value, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Contours
contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
res_dict = {'threshold': thresh_value, 'contours': contours,
            'img_thresh': img_thresh, 'min_area': min_area_proc,
            'approx_factor': approx, 'title': title}
res_list.append(res_dict)

### Process 3 - No Blur / Bin. OTSU + 20 / No min area
title = 'No Blur / Bin. OTSU + 20 / No Min area / Approx = 0.02'
approx = 0.02
min_area_proc = 1
# Otsu
thresh_value, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh_value, img_thresh = cv2.threshold(img_gray, thresh_value+20, 255, cv2.THRESH_BINARY)
# Contours
contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
res_dict = {'threshold': thresh_value, 'contours': contours,
            'img_thresh': img_thresh, 'min_area': min_area_proc,
            'approx_factor': approx, 'title': title}
res_list.append(res_dict)

### Process 4 - Blur / Bin. OTSU
title = 'Blur 15x15 / Bin. OTSU / No Min area / Approx = 0.02'
approx = 0.02
min_area_proc = 1
# Blur - 15x15
img_contrast = cv2.GaussianBlur(img_gray, (15,15), 0)
# Otsu
thresh_value, img_thresh = cv2.threshold(img_contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Contours
contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
res_dict = {'threshold': thresh_value, 'contours': contours,
            'img_thresh': img_thresh, 'min_area': min_area_proc,
            'approx_factor': approx, 'title': title}
res_list.append(res_dict)

### Process 5 - Blur / Bin. OTSU / APPROX !!
title = 'Blur 15x15 / Bin. OTSU / No Min area / Approx = 0.05'
approx = 0.05
min_area_proc = 1
# Blur - 15x15
img_contrast = cv2.GaussianBlur(img_gray, (15,15), 0)
# Otsu
thresh_value, img_thresh = cv2.threshold(img_contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Contours
contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
res_dict = {'threshold': thresh_value, 'contours': contours,
            'img_thresh': img_thresh, 'min_area': min_area_proc,
            'approx_factor': approx, 'title': title}
res_list.append(res_dict)

### Process 5 - Blur / Bin. OTSU / APPROX !!
title = 'Blur 15x15 / Bin. OTSU / No Min area / Approx = 0.1'
approx = 0.1
min_area_proc = 1
# Blur - 15x15
img_contrast = cv2.GaussianBlur(img_gray, (15,15), 0)
# Otsu
thresh_value, img_thresh = cv2.threshold(img_contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Contours
contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
res_dict = {'threshold': thresh_value, 'contours': contours,
            'img_thresh': img_thresh, 'min_area': min_area_proc,
            'approx_factor': approx, 'title': title}
res_list.append(res_dict)

### Generate output image
img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

hist_img = generate_histogram(img_gray, gray=True, thickness=hist_thickness)


# Display Results
mode = ord('a')
process_disp = ord('1')
title_out = ''
nb_process = len(res_list)
while mode != ord('q'):
    # --- Change displayed process ---
    if process_disp != ord('a'):
        val_process = process_disp - ord('1')
        if val_process < nb_process:
            img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
            thresh_value = res_list[val_process]['threshold']
            contours = res_list[val_process]['contours']
            generate_image(img_out, contours, min_area=res_list[val_process]['min_area'],
                           approx_factor=res_list[val_process]['approx_factor'], title=title)
            # Vertical line on Otsu threshold on histogram
            hist_img = generate_histogram(img_gray, gray=True, thickness=hist_thickness)
            x1 = int(thresh_value) * hist_thickness  # 512 pixels for 256 levels (histogram)
            cv2.line(hist_img, (x1, 1), (x1, 400), (0, 255, 255), 1)
            img_thresh = res_list[val_process]['img_thresh']
            title_out = res_list[val_process]['title']
    process_disp = ord('a')

    # --- Processing ---
    if mode == ord('a'):  # Initial image
        final_output = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
        color = (0, 255, 255)
    elif mode == ord('z'):  # Binarized image
        final_output = cv2.cvtColor(img_thresh, cv2.COLOR_GRAY2BGR)
        color = (0, 255, 255)
    else:
        final_output = img_out.copy()
        color = (0, 255, 255)
    cv2.putText(final_output, title_out, (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # --- Display ---
    cv2.imshow("Main image", final_output)
    cv2.imshow("Histogram", hist_img)

    # --- Mode management ---
    key = cv2.waitKey(1) & 0xFF
    if key >= ord('1') and key <= ord('9'):
        process_disp = key
    elif key != 255:
        mode = key

cv2.destroyAllWindows()

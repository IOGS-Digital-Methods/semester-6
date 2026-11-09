import sys
sys.path.append("../_libs/")

import matplotlib.pyplot as plt  # for plotting
from marker_finding import *
from image_lib import scale_image

dir_path = '../_data_marker/'
ref_path = dir_path+'mire_rep_V2_1.png'
image_ref = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
test_path = dir_path+'mire_tik_V2.png'
image_test = cv2.imread(test_path, cv2.IMREAD_GRAYSCALE)

# EVOLUTION
scales = np.arange(0.2, 2.1, 0.1)
result_score = []
for scale in scales:
    new_ref = scale_image(image_ref, scale)
    matches = find_all_matches_multiscale(image_test, new_ref,
                                          threshold=0.5, min_scale=0.7, max_scale=1.3,
                                          num_scales=11)
    if len(matches) > 0:
        result_score.append(matches[0]['score'])
    else:
        result_score.append(0)

plt.figure()
plt.plot(scales, result_score)
plt.show()

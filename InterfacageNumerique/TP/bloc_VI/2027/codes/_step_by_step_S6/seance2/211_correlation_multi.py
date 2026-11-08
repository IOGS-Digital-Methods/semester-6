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

# Display the reference image
plt.figure()
plt.imshow(image_ref, cmap='gray')
plt.title('Reference Image')
plt.axis('off')

# Modify scale of marker
image_ref = scale_image(image_ref, 0.3)

matches = find_all_matches_multiscale(
    image_test,
    image_ref,

    threshold=0.9,

    min_scale=0.5,
    max_scale=3.0,

    num_scales=25,

    max_matches=20,
    iou_threshold=0.3
)

plt.figure()
plt.imshow(image_test, cmap='gray')

for m in matches:
    print(
        f"x={m['x']:4d}, "
        f"y={m['y']:4d}, "
        f"scale={m['scale']:.2f}, "
        f"score={m['score']:.3f}"
    )

    plt.plot(m['x'], m['y'], "ro")

plt.axis("off")
plt.show()


# EVOLUTION
image_ref = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
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

import matplotlib.pyplot as plt  # for plotting
from marker_finding import *

dir_path = './_data/'
ref_path = dir_path+'mire_rep_V2_1.png'
image_ref = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
test_path = dir_path+'mire_tik_V2_big.png'
image_test = cv2.imread(test_path, cv2.IMREAD_GRAYSCALE)

# Display the reference image
plt.figure()
plt.imshow(image_ref, cmap='gray')
plt.title('Reference Image')
plt.axis('off')

# ALGO ?

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

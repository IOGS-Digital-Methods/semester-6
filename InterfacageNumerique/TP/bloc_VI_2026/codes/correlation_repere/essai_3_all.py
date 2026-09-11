import matplotlib.pyplot as plt  # for plotting
from marker_finding import *

dir_path = './_data/'
ref_path = dir_path+'mire_rep_V2_1.png'
image_ref1 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
ref_path = dir_path+'mire_rep_V2_2.png'
image_ref2 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
ref_path = dir_path+'mire_rep_V2_3.png'
image_ref3 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
test_path = dir_path+'mire_tik_V2_big.png'
image_test = cv2.imread(test_path, cv2.IMREAD_GRAYSCALE)


# ALGO ?

matches1 = find_all_matches_multiscale(
    image_test,
    image_ref1
)
matches2 = find_all_matches_multiscale(
    image_test,
    image_ref2
)
matches3 = find_all_matches_multiscale(
    image_test,
    image_ref3
)

plt.figure()
plt.imshow(image_test, cmap='gray')

print(f'Motif 1')
for m in matches1:
    print(
        f"x={m['x']:4d}, "
        f"y={m['y']:4d}, "
        f"scale={m['scale']:.2f}, "
        f"score={m['score']:.3f}"
    )

    plt.plot(m['x'], m['y'], "ro")

print(f'Motif 2')
for m in matches2:
    print(
        f"x={m['x']:4d}, "
        f"y={m['y']:4d}, "
        f"scale={m['scale']:.2f}, "
        f"score={m['score']:.3f}"
    )

    plt.plot(m['x'], m['y'], "go")

print(f'Motif 3')
for m in matches3:
    print(
        f"x={m['x']:4d}, "
        f"y={m['y']:4d}, "
        f"scale={m['scale']:.2f}, "
        f"score={m['score']:.3f}"
    )

    plt.plot(m['x'], m['y'], "bo")

plt.axis("off")
plt.show()

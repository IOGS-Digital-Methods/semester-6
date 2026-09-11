import matplotlib.pyplot as plt  # for plotting
from marker_finding import *

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

# Recherche des maximums locaux de corrélation
threshold = 0.8
corr_res = find_locales(result, threshold)

## AFFICHAGE
plt.figure()
plt.imshow(image_test, cmap='gray')

for m in corr_res:
    print(m)
    plt.plot(m[0], m[1], "ro")
    #plt.text(x + 10, y - 10, f"({m['x']}, {m['y']})", color="red")

plt.axis("off")
plt.show()

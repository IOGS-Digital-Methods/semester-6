import scipy.io  # for reading .mat files
import numpy as np  # for numerical operations
from scipy.fft import fft2, ifft2, fftshift  # for Fourier Transform
import matplotlib.pyplot as plt  # for plotting


# Helper function to register two images
def registration(img, ref, display=False):
    # Zero-mean the images
    img1 = img - np.mean(img)
    img2 = ref - np.mean(ref)

    # Calculate the Fourier Transform of the images
    img1_fft = fft2(img1, s=2*np.array(img1.shape)-1)
    img2_fft = fft2(img2, s=2*np.array(img2.shape)-1)

    # Calculate the cross-correlation using the FFT
    crr = fftshift(ifft2(img1_fft * np.conj(img2_fft)))

    # Display the cross-correlation
    if display:
        plt.figure()
        plt.imshow(np.abs(crr), cmap='viridis')
        plt.title('Cross-correlation')
        plt.colorbar()

    # Find the peak of the cross-correlation
    peak = np.unravel_index(np.argmax(crr), crr.shape)

    # Calculate the shift
    shift = np.array(crr.shape)//2 - np.array(peak)

    return shift

# Helper function to shift an image
def shift_image(img, shift):
    # Shift the image
    shifted_img = np.roll(img, shift, axis=(0,1))

    # Zero out the pixels that are shifted out of the image
    if shift[0] < 0:
        shifted_img[shift[0]:, :] = 0
    else:
        shifted_img[:shift[0], :] = 0

    if shift[1] < 0:
        shifted_img[:, shift[1]:] = 0
    else:
        shifted_img[:, :shift[1]] = 0

    return shifted_img


samples = scipy.io.loadmat('data/ShiftedImages.mat')
image_ref = samples['Images'][1:,:,0] # FIXME: Remove the first rows
images = samples['Images'][1:,:,1:] # FIXME: Remove the first rows

# Display the reference image
plt.figure()
plt.imshow(image_ref, cmap='gray')
plt.title('Reference Image')
plt.axis('off')
plt.show()

# Display the cross-correlation of the first image with the reference image
registration(images[:,:,0], image_ref, display=True)

# Register the images
shifts = []
for i in range(images.shape[2]):
    shift = registration(images[:,:,i], image_ref)
    shifts.append(shift)

# Display the registered images
fig, axs = plt.subplots(1, images.shape[2], figsize=(20, 5))
for i in range(images.shape[2]):
    axs[i].imshow(shift_image(images[:,:,i], shifts[i]), cmap='gray')
    axs[i].set_title(f'Image {i+1}')
    axs[i].axis('off')
plt.show()
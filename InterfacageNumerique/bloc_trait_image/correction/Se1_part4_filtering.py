# -*- coding: utf-8 -*-
"""*Se1_part4_filtering.py* file.

This file contains a script to open an image with OpenCV and to process median, mean and gaussian blur filters on an image.

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on image processing, see : https://iogs-lense-training.github.io/image-processing/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 20/oct/2024
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt


def process_hist_from_array(array: np.ndarray, bins: list) -> (np.ndarray, np.ndarray):
    """
    Calculate a histogram from an array and bins definition.
    :param array: Array containing data.
    :param bins: Bins to calculate the histogram.
    :return: Tuple of np.ndarray: bins and hist data.
    """
    plot_hist, plot_bins_data = np.histogram(array, bins=bins)
    return plot_bins_data, plot_hist

def display_hist(data: np.ndarray, data_hist: np.ndarray, bins: np.ndarray,
              title: str = 'Image Histogram'):
    """
    Display a histogram from data.
    :param data: Data to process.
    :param data_hist: Histogram data from np.histogram function.
    :param bins: Bins of the histogram.
    :param title: Title of the figure. Default: Image Histogram.
    :param file_name: Name of the file to store the PNG image. Default: histogram.png.
    :param informations: Informations to display in the graph.
    """
    n = len(bins)
    mean_data = np.mean(data)
    if mean_data > bins[n//2]:
        x_text_pos = 0.30  # text on the left
    else:
        x_text_pos = 0.95  # text on the right
    plt.figure(figsize=(10, 8), dpi=150)
    plt.bar(bins[:-1], data_hist, width=np.diff(bins),
            edgecolor='black', alpha=0.75, color='blue')
    plt.title(title)
    text_str = f'Mean = {mean_data:.2f}\nStdDev = {np.std(data):.2f}'
    plt.text(x_text_pos, 0.95, text_str, fontsize=10, verticalalignment='top',
             horizontalalignment='right',
             transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
    plt.show()

def zoom_array(im_array: np.ndarray, zoom_factor: int = 1):
    """Zoom inside an array in 2D.
    :param im_array: Array to change.
    :param zoom_factor: Zoom factor.
    :return: Modified array.
    """
    return np.repeat(np.repeat(im_array, zoom_factor, axis=0), zoom_factor, axis=1)

if __name__ == "__main__":
    # Open an image - Grayscale
    image_gray = cv2.imread('../../_images/a_letter_noise.jpg', cv2.IMREAD_GRAYSCALE)      
    image_gray = cv2.imread('../../_images/robot.jpg', cv2.IMREAD_GRAYSCALE)
          
    k_size = 21
    # Gaussian Blur
    gaussian_image = cv2.GaussianBlur(image_gray, (k_size, k_size), sigmaX=1) 

    diff = image_gray - gaussian_image
    
    fig, ax = plt.subplots(nrows=1, ncols=3)    
    ax[0].imshow(image_gray, cmap='gray')
    ax[0].set_title('Gray original image')  
    ax[1].imshow(gaussian_image, cmap='gray')
    ax[1].set_title('Gaussian Blur')
    ax[2].imshow(diff, cmap='gray')
    ax[2].set_title('Gaussian Blur / Diff')
   

    plt.show()   
    
    
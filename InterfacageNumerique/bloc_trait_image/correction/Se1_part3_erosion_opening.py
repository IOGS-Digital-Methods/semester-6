# -*- coding: utf-8 -*-
"""*Se1_part3_erosion_opening.py* file.

This file contains a script to open an image with OpenCV and to process erosion, dilation, opening and closing processes on images.

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on image processing, see : https://iogs-lense-training.github.io/image-processing/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 20/oct/2024
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

def generate_gaussian_noise_image_percent(rows, cols, percent_pixels=10, mean=0, std_dev=1):
    """
    Create a 2D array with a gaussian noise - on a part of the image.
    
    :param rows: Number of rows.
    :param cols: Number of columns.
    :param mean: Mean of the gaussian distribution.
    :param std_dev: Standard deviation of the gaussian distribution.
    :percent_pixels: Percent of pixels where to add noise.
    :return: 2D array.
    """
    image = np.zeros((rows, cols))
    
    total_pixels = rows * cols
    num_pixels = (percent_pixels * total_pixels) // 100
    indices = np.random.choice(total_pixels, num_pixels, replace=False)
    
    row_indices = indices // cols
    col_indices = indices % cols
   
    image[row_indices, col_indices] = np.random.normal(mean, std_dev, num_pixels)

    return image

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
    
    # Generate structuring elements
    cross_3 = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    print(type(cross_3))
    print(cross_3)
    rect_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    print(rect_3)  

    # Erosion
    eroded_image_cross_3 = cv2.erode(image_gray, cross_3, iterations=1)
    eroded_image_rect_3 = cv2.erode(image_gray, rect_3, iterations=1)
    
    fig, ax = plt.subplots(nrows=1, ncols=3)    
    ax[0].imshow(image_gray, cmap='gray')
    ax[0].set_title('Gray original image')  
    ax[1].imshow(eroded_image_cross_3, cmap='gray')
    ax[1].set_title('3-cross erosion')
    ax[2].imshow(eroded_image_rect_3, cmap='gray')
    ax[2].set_title('3-rect erosion')
   
    # Dilation
    dilated_image_cross_3 = cv2.dilate(image_gray, cross_3, iterations=1)
    dilated_image_rect_3 = cv2.dilate(image_gray, rect_3, iterations=1)
    
    fig, ax = plt.subplots(nrows=1, ncols=3)    
    ax[0].imshow(image_gray, cmap='gray')
    ax[0].set_title('Gray original image')  
    ax[1].imshow(dilated_image_cross_3, cmap='gray')
    ax[1].set_title('3-cross dilation')
    ax[2].imshow(dilated_image_rect_3, cmap='gray')
    ax[2].set_title('3-rect dilation')

    # Opening
    opening_image_cross_3 = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, cross_3)
    opening_image_rect_3 = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, rect_3)
    
    fig, ax = plt.subplots(nrows=1, ncols=3)    
    ax[0].imshow(image_gray, cmap='gray')
    ax[0].set_title('Gray original image')  
    ax[1].imshow(opening_image_cross_3, cmap='gray')
    ax[1].set_title('3-cross opening')
    ax[2].imshow(opening_image_rect_3, cmap='gray')
    ax[2].set_title('3-rect opening')

    # Closing
    closing_image_cross_3 = cv2.morphologyEx(image_gray, cv2.MORPH_CLOSE, cross_3)
    closing_image_rect_3 = cv2.morphologyEx(image_gray, cv2.MORPH_CLOSE, rect_3)
    
    fig, ax = plt.subplots(nrows=1, ncols=3)    
    ax[0].imshow(image_gray, cmap='gray')
    ax[0].set_title('Gray original image')  
    ax[1].imshow(closing_image_cross_3, cmap='gray')
    ax[1].set_title('3-cross closing')
    ax[2].imshow(closing_image_rect_3, cmap='gray')
    ax[2].set_title('3-rect closing')

    # Gradient    
    image_gray = cv2.imread('../../_images/robot.jpg', cv2.IMREAD_GRAYSCALE)
    
    gradient_image_cross_3 = cv2.morphologyEx(image_gray, cv2.MORPH_GRADIENT, cross_3)
    gradient_image_rect_3 = cv2.morphologyEx(image_gray, cv2.MORPH_GRADIENT, rect_3)
    
    fig, ax = plt.subplots(nrows=1, ncols=3)    
    ax[0].imshow(image_gray, cmap='gray')
    ax[0].set_title('Gray original image')  
    ax[1].imshow(gradient_image_cross_3, cmap='gray')
    ax[1].set_title('3-cross gradient')
    ax[2].imshow(gradient_image_rect_3, cmap='gray')
    ax[2].set_title('3-rect gradient')

    plt.show()   
    
    
# -*- coding: utf-8 -*-
"""*Se1_part1_generer_bruit.py* file.

This file contains a script to open an image with OpenCV and to add noise on the image.

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on image processing, see : https://iogs-lense-training.github.io/image-processing/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 20/oct/2024
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

def generate_gaussian_noise_image(rows, cols, mean=0, std_dev=1):
    """
    Create a 2D array with a gaussian noise.
    
    :param rows: Number of rows.
    :param cols: Number of columns.
    :param mean: Mean of the gaussian distribution.
    :param std_dev: Stander deviation of the gaussian distribution.
    :return: 2D array.
    """
    gaussian_noise = np.random.normal(mean, std_dev, (rows, cols))    
    return gaussian_noise

def generate_uniform_noise_image(rows, cols, min_val=0, max_val=1):
    """
    Create a 2D array with a uniform noise.
    
    :param rows: Number of rows.
    :param cols: Number of columns.
    :param min_val: Minimum value of the uniform distribution.
    :param max_val: Maximum value of the uniform distribution.
    :return: 2D array.
    """
    uniform_noise = np.random.uniform(min_val, max_val, (rows, cols))    
    return uniform_noise

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


if __name__ == "__main__":
    # Open an image - Grayscale
    image_gray = cv2.imread('../../_images/robot.jpg', cv2.IMREAD_GRAYSCALE)
    # Gaussian Noise
    gauss_noise = generate_gaussian_noise_image_percent(image_gray.shape[0], image_gray.shape[1], 10, 50, 10)

    # Histogram 
    image_bits_depth = 8
    bins = np.linspace(0, 2 ** image_bits_depth, 2 ** image_bits_depth+1)
    bins, data = process_hist_from_array(gauss_noise, bins)
    display_hist(gauss_noise, data[1:], bins[1:])
    
    # Uniform Noise
    uni_noise = generate_uniform_noise_image(image_gray.shape[0], image_gray.shape[1], 10, 20)
    # Histogram 
    image_bits_depth = 8
    bins = np.linspace(0, 2 ** image_bits_depth, 2 ** image_bits_depth+1)
    bins, data = process_hist_from_array(uni_noise, bins)
    display_hist(uni_noise, data, bins)
    
    
    image_noise = image_gray + gauss_noise
    image_noise = image_noise.astype(np.uint8)
    
    # Display the noise image
    cv2.imshow('Noise image', gauss_noise)
    cv2.waitKey(0)
    # Display the image with noise
    cv2.imshow('Image with noise', image_noise)
    cv2.waitKey(0)    
    
    cv2.destroyAllWindows()
    
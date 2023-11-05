from skimage.transform import hough_line, hough_line_peaks
import numpy as np

def perform_hough_transform(edge_image, angles):
    return hough_line(edge_image, angles)

def get_hough_peaks(hspace, theta, dist, threshold=500):
    return hough_line_peaks(hspace, theta, dist, threshold=threshold)
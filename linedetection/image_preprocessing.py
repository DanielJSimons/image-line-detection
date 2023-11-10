import cv2
import numpy as np

# Image preprocessing constants
SIZE_GBLUR = 3
SIZE_BLBLUR = 3
SIGMACOLOUR = 80 
SIGMASPACE = 80
MIN_LEN = 25
DEG = 10
HOUGH_THRES = 700
HOUGH_POINTS = 180
MAX_R = 20
APERTURE_SIZE = 3

def adjust_parameters(analysis_results, MIN_LEN=MIN_LEN, DEG=DEG, MAX_R=MAX_R, HOUGH_THRES=HOUGH_THRES, HOUGH_POINTS=HOUGH_POINTS, APERTURE_SIZE = APERTURE_SIZE,SIZE_GBLUR = SIZE_GBLUR, SIZE_BLBLUR = SIZE_BLBLUR, SIGMACOLOUR = SIGMACOLOUR, SIGMASPACE = SIGMASPACE):
        # Extracting variables for easier referencing
    edge_variance = analysis_results['edge_variance']
    edge_mean_intensity = analysis_results['edge_mean_intensity']
    average_line_width = analysis_results['average_line_width']
    avg_region_size = analysis_results['avg_region_size']

    # High Edge Variance and Intensity
    if edge_variance > 0.05 or edge_mean_intensity > 0.1:
        SIZE_GBLUR -= 2
        SIZE_BLBLUR -= 2
        SIGMACOLOUR += 10
        SIGMASPACE += 20
        MIN_LEN -= 7
        DEG += 2
        HOUGH_THRES -= 50
        MAX_R -= 10

    # Medium Edge Variance and Intensity
    elif 0.02 < edge_variance <= 0.05 or 0.05 < edge_mean_intensity <= 0.1:
        SIZE_GBLUR += 2
        if average_line_width > 0.8:
            SIZE_BLBLUR += 2
            SIGMACOLOUR -= 20
            SIGMASPACE -= 20
            MIN_LEN -= 5
            DEG -= 3
            HOUGH_THRES -= 50
        elif average_line_width < 0.7:
            SIGMACOLOUR += 20
            SIGMASPACE += 20
            MIN_LEN += 5
            DEG += 3

    # Low Edge Variance and Intensity
    elif edge_variance <= 0.03 and edge_mean_intensity <= 0.06:
        SIZE_GBLUR -= 2
        SIZE_BLBLUR -= 2
        SIGMACOLOUR += 10
        SIGMASPACE += 10
        MIN_LEN += 10
        DEG += 3
        APERTURE_SIZE+=2

    # Adjust based on Average Region Size
    if avg_region_size < 10:
        SIZE_GBLUR += 2
        SIZE_BLBLUR += 2
    elif avg_region_size > 100:
        SIZE_GBLUR -= 2
        SIZE_GBLUR = max(1, SIZE_GBLUR)
        SIGMACOLOUR -= 10
        SIGMASPACE -= 10
    elif avg_region_size > 3000:
        MAX_R += 20
        HOUGH_POINTS += 20
    elif avg_region_size < 1000:
        MAX_R -= 5
        HOUGH_POINTS -= 20

    MIN_LEN = max(1, MIN_LEN)
    DEG = max(1, DEG)
    HOUGH_THRES = max(1, HOUGH_THRES)
    HOUGH_POINTS = max(1, HOUGH_POINTS)
    APERTURE_SIZE = max(1, APERTURE_SIZE)
    SIZE_GBLUR = max(1, SIZE_GBLUR)
    SIZE_BLBLUR = max(1, SIZE_BLBLUR)
    SIGMACOLOUR = max(1, SIGMACOLOUR)
    SIGMASPACE = max(1, SIGMASPACE)
    
    return SIZE_GBLUR, SIZE_BLBLUR, SIGMACOLOUR, SIGMASPACE, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS

def load_image(filepath):
    original_image = cv2.imread(filepath, 0)
    if original_image is None:
        raise ValueError("Error loading the image!")
    return original_image

def enhance_contrast(image, alpha=1.5, beta=50):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def sharpen_image(image):
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    return cv2.filter2D(image, -1, kernel)

def load_and_invert_image(filepath):
    image = cv2.imread(filepath, 0)
    if image is None:
        raise ValueError("Error loading the image!")
    inverted_image = ~image
    return enhance_contrast(inverted_image)

def blur_image(image, size_gblur=SIZE_GBLUR, size_blblur=SIZE_BLBLUR, sigmacolour=SIGMACOLOUR, sigmaspace=SIGMASPACE):
    x_gblurred = cv2.GaussianBlur(image, (1, size_gblur), 0)
    x_bfblurred = cv2.bilateralFilter(x_gblurred, size_blblur, sigmacolour, sigmaspace)
    return x_bfblurred

def dilate_image(image):
    kernel = np.ones((1,3), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

def detect_edges(blurred_image):
    v = np.median(blurred_image)
    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))
    x_edges = cv2.Canny(blurred_image, lower, upper, apertureSize = APERTURE_SIZE)
    return dilate_image(x_edges)
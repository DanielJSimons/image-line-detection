import hough_transform
import initial_analysis
import line_detection
import image_preprocessing
import merge_lines
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Function to manually select an image file
def select_image_file():
    # Hide the root Tkinter window
    Tk().withdraw() 
    # Show an "Open" dialog box and return the path to the selected file
    filename = askopenfilename()
    return filename

def process_image(image_path, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS):
    # Analyse image
    analysis_results = initial_analysis.analyze_image(image_path)

    # Adjust parameters based on analysis_results
    SIZE_GBLUR, SIZE_BLBLUR, SIGMACOLOUR, SIGMASPACE, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS = image_preprocessing.adjust_parameters(analysis_results, MIN_LEN=MIN_LEN, DEG=DEG, MAX_R=MAX_R, HOUGH_THRES=HOUGH_THRES, HOUGH_POINTS=HOUGH_POINTS)

    # Load and preprocess the image
    original_image = image_preprocessing.load_image(image_path)
    image = image_preprocessing.load_and_invert_image(image_path)
    blurred_image = image_preprocessing.blur_image(image, SIZE_GBLUR, SIZE_BLBLUR, SIGMACOLOUR, SIGMASPACE)
    edge_image = image_preprocessing.detect_edges(blurred_image)

    # Hough Transform and line detection
    angles = np.linspace(-np.pi / 2, np.pi / 2, HOUGH_POINTS)
    hspace, theta, dist = hough_transform.perform_hough_transform(edge_image, angles)

    # Find lines and merge them
    h_values, peak_angles, peak_dists = hough_transform.get_hough_peaks(hspace, theta, dist, threshold=HOUGH_THRES)
    clusters = merge_lines.cluster_lines(peak_angles, peak_dists, np.deg2rad(DEG), MAX_R)

    # Create figure for displaying the images
    fig, (ax_orig, ax_lines) = plt.subplots(1, 2, figsize=(10, 5))

    # Display original image
    ax_orig.imshow(original_image, cmap='gray')
    ax_orig.set_title('Original Image')
    ax_orig.axis('off')

    # Display lines on the image
    ax_lines.imshow(original_image, cmap='gray')
    ax_lines.set_title('Detected Lines')
    ax_lines.axis('off')

    for cluster in clusters:
        angle, dist = merge_lines.average_lines_in_cluster(cluster, peak_angles, peak_dists)
        x0, y0, x1, y1 = line_detection.intersection_points(angle, dist, edge_image.shape)
        if x0 is not None and line_detection.is_line_valid(x0, y0, x1, y1, edge_image, min_length=MIN_LEN):
            ax_lines.plot((x0, x1), (y0, y1), '-r')

    output_path = image_path.replace('.jpg', '_processed.jpg')
    plt.savefig(output_path)
    plt.close(fig)

def process_image_pdf(image_path, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS):
        # Analyse image
    analysis_results = initial_analysis.analyze_image(image_path)

    # Adjust parameters based on analysis_results
    SIZE_GBLUR, SIZE_BLBLUR, SIGMACOLOUR, SIGMASPACE, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS = image_preprocessing.adjust_parameters(analysis_results, MIN_LEN=MIN_LEN, DEG=DEG, MAX_R=MAX_R, HOUGH_THRES=HOUGH_THRES, HOUGH_POINTS=HOUGH_POINTS)

    # Load and preprocess the image
    original_image = image_preprocessing.load_image(image_path)
    image = image_preprocessing.load_and_invert_image(image_path)
    blurred_image = image_preprocessing.blur_image(image, SIZE_GBLUR, SIZE_BLBLUR, SIGMACOLOUR, SIGMASPACE)
    edge_image = image_preprocessing.detect_edges(blurred_image)

    # Hough Transform and line detection
    angles = np.linspace(-np.pi / 2, np.pi / 2, HOUGH_POINTS)
    hspace, theta, dist = hough_transform.perform_hough_transform(edge_image, angles)

    # Find lines and merge them
    h_values, peak_angles, peak_dists = hough_transform.get_hough_peaks(hspace, theta, dist, threshold=HOUGH_THRES)
    clusters = merge_lines.cluster_lines(peak_angles, peak_dists, np.deg2rad(DEG), MAX_R)
    line_data = []
    for cluster in clusters:
        angle, dist = merge_lines.average_lines_in_cluster(cluster, peak_angles, peak_dists)
        x0, y0, x1, y1 = line_detection.intersection_points(angle, dist, edge_image.shape)
        if x0 is not None and line_detection.is_line_valid(x0, y0, x1, y1, edge_image, min_length=MIN_LEN):
            line_data.append((x0, y0, x1, y1))

    # Return the original image path and the line data for later visualization
    return {
        "original_image_path": image_path,  # Path to the original image
        "line_data": line_data              # Coordinates of the detected lines
    }
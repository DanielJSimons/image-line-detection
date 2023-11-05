import hough_transform
import initial_analysis
import line_detection
import image_preprocessing
import merge_lines
import numpy as np

from matplotlib import pyplot as plt
#import visualization


def process_images(MIN_LEN=image_preprocessing.MIN_LEN, DEG=image_preprocessing.DEG, MAX_R=image_preprocessing.MAX_R, HOUGH_THRES=image_preprocessing.HOUGH_THRES, HOUGH_POINTS=image_preprocessing.HOUGH_POINTS):
# Set up a 2x9 grid
    fig, axes = plt.subplots(2, 8, figsize=(20, 10))

    # Loop through the image range
    for i in range(1, 9):
        # Load the image
        image_path = f"C:/Users/Daniel Simons/Documents/Line_Detection/Images/line_detection_table{i}.jpg"
        original_image = image_preprocessing.load_image(image_path)

        # Analyse image
        analysis_results = initial_analysis.analyze_image(image_path)

        # Adjust parameters based on analysis_results
        SIZE_GBLUR, SIZE_BLBLUR, SIGMACOLOUR, SIGMASPACE, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS = image_preprocessing.adjust_parameters(analysis_results, MIN_LEN=MIN_LEN, DEG=DEG, MAX_R=MAX_R, HOUGH_THRES=HOUGH_THRES, HOUGH_POINTS=HOUGH_POINTS)

        # Preprocess the image with inversion
        image = image_preprocessing.load_and_invert_image(image_path)
        blurred_image = image_preprocessing.blur_image(image, SIZE_GBLUR, SIZE_BLBLUR, SIGMACOLOUR, SIGMASPACE) # example usage
        edge_image = image_preprocessing.detect_edges(blurred_image)

        # Hough Transform and line detection
        angles = np.linspace(-np.pi / 2, np.pi / 2, HOUGH_POINTS)
        hspace, theta, dist = hough_transform.perform_hough_transform(edge_image, angles)

        # Display original image
        ax_orig = axes[0, i-1]
        ax_orig.imshow(original_image, cmap='gray')
        ax_orig.set_title(f'Image {i}')
        ax_orig.axis('off')

        # Line merging logic
        h_values, peak_angles, peak_dists = hough_transform.get_hough_peaks(hspace, theta, dist, threshold=HOUGH_THRES)
        clusters = merge_lines.cluster_lines(peak_angles, peak_dists, np.deg2rad(DEG), MAX_R)

        ax_lines = axes[1, i-1]
        ax_lines.imshow(original_image, cmap='gray')
        ax_lines.set_title(f'Lines {i}')
        ax_lines.axis('off')

        for cluster in clusters:
            angle, dist = merge_lines.average_lines_in_cluster(cluster, peak_angles, peak_dists)
            x0, y0, x1, y1 = line_detection.intersection_points(angle, dist, edge_image.shape)
            if x0 is not None and line_detection.is_line_valid(x0, y0, x1, y1, edge_image, min_length=MIN_LEN):
                ax_lines.plot((x0, x1), (y0, y1), '-r')

process_images(MIN_LEN=40, DEG=15, MAX_R=20, HOUGH_THRES=400, HOUGH_POINTS=180)

# Tight layout for better appearance
plt.tight_layout()
plt.show()
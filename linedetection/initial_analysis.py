import numpy as np
from skimage import filters, color, morphology, measure
import cv2
#from matplotlib import pyplot as plt

def analyze_image(image_path):
    image = cv2.imread(image_path, 0)

    if image is None:
        print(f"Error loading the image {image_path}!")
        return

    image = ~image  

    if len(image.shape) == 2 or image.shape[2] == 1:
        grayscale_image = image
    else:
        grayscale_image = color.rgb2gray(image)

    # Edge Detection using Sobel
    edges = filters.sobel(grayscale_image)

    # Thresholding
    threshold = filters.threshold_otsu(edges)
    binary_edges = edges > threshold

    # Dilate the edges for better connected components
    dilated = morphology.dilation(binary_edges, morphology.square(3))

    edge_variance = np.var(edges)
    edge_mean_intensity = np.mean(edges)

    # Morphological Operations to measure average line width
    eroded = morphology.erosion(edges, morphology.square(3))
    difference = edges - eroded
    average_line_width = np.sum(difference) / np.sum(edges)

    # Connected Component Analysis for region sizes on the dilated edges
    labeled = measure.label(dilated)
    properties = measure.regionprops(labeled)
    region_sizes = [prop.area for prop in properties]

    if len(region_sizes) == 0:
        avg_region_size = 0  
    else:
        avg_region_size = np.mean(region_sizes)

    return {
        "edge_variance": edge_variance,
        "edge_mean_intensity": edge_mean_intensity,
        "average_line_width": average_line_width,
        "avg_region_size": avg_region_size
    }

base_path = 'C:/Users/Daniel Simons/Documents/Line_Detection/Images/'
images = [base_path + f'line_detection_table{i}.jpg' for i in range(8, 9)]

for image_path in images:
    analyze_image(image_path)



    """
    print(f"\nAnalysis for {image_path}:")
    print("====================================")
    print(f"Edge Variance: {edge_variance}")
    print(f"Edge Mean Intensity: {edge_mean_intensity}")
    print(f"Average Line Width: {average_line_width}")
    print(f"Average Region Size from Connected Components: {avg_region_size}")


    # For Visual Inspection: Overlay labels on the original image
    labeled_overlay = color.label2rgb(labeled, image=grayscale_image, bg_label=0)

    # For Histogram: Distribution of region sizes
    plt.figure()
    plt.hist(region_sizes, bins=50, facecolor='blue', alpha=0.7)
    plt.title('Histogram of Region Sizes')
    plt.xlabel('Region Size (pixels)')
    plt.ylabel('Frequency')
    plt.grid(True)

    # Display the results
    plt.figure()
    plt.imshow(labeled_overlay)
    plt.title('Labeled Regions Overlay')
    plt.show()
    """

"""
low edge variance: increase contrast, sharpen image, lower threshold to detect edges with canny
high edge variance: noise reduction, adaptive thresholding for edge detection, gaussian blurring to reduce texture

Low Edge Mean Intensity: Enhance contrast, increase sensitivity in edge detection, decrease blur
high edge mean intensity: reduce noise, increase sensitivity in edge detection if too many edges, post processing erosion can thin edges, decrease contrast

low average line width: increase edge sensitivity, reduce blur, morphological dilation
high average line width: increase blur, adjust edge sensitivity to reduce lines breaking with canny.

low average region size: increase blur, morphological closing
high average region size: reduce blur, increase edge detection sensitivity
"""
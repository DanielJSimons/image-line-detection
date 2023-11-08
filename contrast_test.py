import numpy as np
import cv2

contrast_image_path = "Images\\line_detection_table1.jpg"
test_image = cv2.imread(contrast_image_path, cv2.IMREAD_GRAYSCALE)

# Calculate the histograms
original_histogram = cv2.calcHist([test_image], [0], None, [256], [0, 256])

alpha = 2.0  # Adjust alpha value as needed
beta = 0

# Apply contrast adjustment
contrast_image = cv2.convertScaleAbs(test_image, alpha=alpha, beta=beta)

# Calculate the histogram of the adjusted image
contrast_histogram = cv2.calcHist([contrast_image], [0], None, [256], [0, 256])

# Normalize histograms to have a sum of 1 (L1 normalization)
original_histogram_normalized = original_histogram / np.sum(original_histogram)
contrast_histogram_normalized = contrast_histogram / np.sum(contrast_histogram)

# Calculate histogram intersection
intersection = np.minimum(original_histogram_normalized, contrast_histogram_normalized)
intersection_score = np.sum(intersection)

# Calculate Bhattacharyya distance
bhattacharyya_distance = -np.log(np.sum(np.sqrt(original_histogram_normalized * contrast_histogram_normalized)))

print("Histogram Intersection Score:", intersection_score)
print("Bhattacharyya Distance:", bhattacharyya_distance)

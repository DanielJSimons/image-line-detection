import cv2
import numpy as np
from image_preprocessing import adjust_parameters, load_image, load_and_invert_image, enhance_contrast, sharpen_image, blur_image, dilate_image, detect_edges
import pytest

class TestAdjustParameters:
    def test_adjust_parameters_high_variance(self):
        analysis_results = {
            'edge_variance': 0.1,
            'edge_mean_intensity':0.07,
            'average_line_width': 0.77,
            'avg_region_size': 1440
        }
        e_results = (1, 1, 80, 90, 18, 12, 10, 350, 180)
        assert adjust_parameters(analysis_results) == e_results

    def test_adjust_parameters_high_mean_intensity(self):
        analysis_results = {
            'edge_variance': 0.03,
            'edge_mean_intensity':0.7,
            'average_line_width': 0.77,
            'avg_region_size': 1440
        }
        e_results = (1, 1, 80, 90, 18, 12, 10, 350, 180)
        assert adjust_parameters(analysis_results) == e_results

    def test_adjust_parameters_high_average_line_width(self):
        analysis_results = {
            'edge_variance': 0.03,
            'edge_mean_intensity':0.7,
            'average_line_width': 1.0,
            'avg_region_size': 1440
        }
        e_results = (1, 1, 80, 90, 18, 12, 10, 350, 180)
        assert adjust_parameters(analysis_results) == e_results     

    def test_adjust_parameters_high_average_region_size(self):
        analysis_results = {
            'edge_variance': 0.03,
            'edge_mean_intensity':0.7,
            'average_line_width': 1.0,
            'avg_region_size': 5000
        }
        e_results = (1, 1, 80, 90, 18, 12, 10, 350, 180)
        assert adjust_parameters(analysis_results) == e_results

    def test_adjust_parameters_low_variance(self):
        analysis_results = {
            'edge_variance': 0.01,
            'edge_mean_intensity':0.07,
            'average_line_width': 0.77,
            'avg_region_size': 1440
        }
        e_results = (3, 3, 70, 70, 25, 10, 20, 400, 180)
        assert adjust_parameters(analysis_results) == e_results

        # Remaining tests to be finished


class TestLoadImage:
    def test_valid_image_path(self):
        valid_image_path = "Images\\line_detection_table1.jpg"
        result = load_image(valid_image_path)
        assert result is not None
        assert isinstance(result, np.ndarray)

class TestEnhanceContrast:
    @pytest.fixture(scope="class")
    def test_image(self):
        contrast_image_path = "Images/line_detection_table1.jpg"
        test_image = cv2.imread(contrast_image_path, cv2.IMREAD_GRAYSCALE)
        if test_image is None:
            pytest.skip("Test image could not be loaded.")
        return test_image

    def calculate_histogram_metrics(self, original_hist, contrast_hist):
        # Normalize histograms to have a sum of 1 (L1 normalization)
        original_histogram_normalized = original_hist / np.sum(original_hist)
        contrast_histogram_normalized = contrast_hist / np.sum(contrast_hist)

        # Calculate histogram intersection
        intersection = np.minimum(original_histogram_normalized, contrast_histogram_normalized)
        intersection_score = np.sum(intersection)

        # Calculate Bhattacharyya distance
        bhattacharyya_distance = -np.log(np.sum(np.sqrt(original_histogram_normalized * contrast_histogram_normalized)))

        return intersection_score, bhattacharyya_distance

    def test_enhance_contrast_normal_case(self, test_image):
        alpha_values = [0.1, 0.5, 1.0, 2.0, 5.0]
        beta_values = [10, 25, 50, 100, 200]

        original_histogram = cv2.calcHist([test_image], [0], None, [256], [0, 256])

        for alpha in alpha_values:
            for beta in beta_values:
                contrast_image = cv2.convertScaleAbs(test_image, alpha=alpha, beta=beta)
                contrast_histogram = cv2.calcHist([contrast_image], [0], None, [256], [0, 256])

                intersection_score, bhattacharyya_distance = self.calculate_histogram_metrics(original_histogram, contrast_histogram)

                assert intersection_score > 0.0
                assert bhattacharyya_distance > 0.0

                assert contrast_image is not None
                assert contrast_image.dtype == np.uint8
                assert contrast_image.shape == test_image.shape
    
class TestSharpenImage:
    def test_sharpen_image(self):
        return 0

class TestInvertImage:
    def test_load_and_invert_image(self):
        return 0
    
class TestBlurImage:
    def test_blur_image(self):
        return 0
    
class TestDilateImage:
    def test_dilate_image(self):
        return 0
    
class TestDetectEdges:
    def test_detect_edges(self):
        return 0
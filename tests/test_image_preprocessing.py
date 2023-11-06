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
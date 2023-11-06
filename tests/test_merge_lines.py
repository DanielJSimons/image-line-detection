import pytest
import numpy as np
from merge_lines import are_lines_close, cluster_lines, average_lines_in_cluster



# Test are_lines_close method
class TestAreLinesClose:
    def test_identical_lines():
        assert are_lines_close(10, 5, 10, 5, 0.1, 0.1) is True

    def test_within_threshold():
        assert are_lines_close(10, 5, 10.09, 5.09, 0.1, 0.1) is True

    def test_outside_threshold():
        assert are_lines_close(10, 5, 10.11, 5.11, 0.1, 0.1) is False

    def test_negative_values():
        assert are_lines_close(-10, -5, -10, -5, 0.1, 0.1) is True

    def test_zero_threshold():
        with pytest.raises(ValueError):
            are_lines_close(10, 5, 10, 5, 0, 0)

    def test_invalid_input():
        with pytest.raises(TypeError):
            are_lines_close("10", 5, 10, 5, 0.1, 0.1)

# Test cluster_lines method


# Test average_lines_in_cluster method
class TestAverageLinesInCluster:
    def test_normal_case():
        angles = np.array([2,4,6,8])
        distance = np.array([12,15,18,21])
        cluster = [2, 3]
        e_angle_mean = np.mean([6,8])
        e_distance_mean = np.mean([18,21])
        assert average_lines_in_cluster(cluster, angles, distance) == (e_angle_mean, e_distance_mean)

    def test_negative_positive_case():
        angles = np.array([-2,4,-6,8])
        distance = np.array([12,-15,18,-21])
        cluster = [2, 3]
        e_angle_mean = np.mean([-6,8])
        e_distance_mean = np.mean([18,-21])
        assert average_lines_in_cluster(cluster, angles, distance) == (e_angle_mean, e_distance_mean)

    def test_negative_negative_case():
        angles = np.array([-2,-4,-6,-8])
        distance = np.array([-12,-15,-18,-21])
        cluster = [2, 3]
        e_angle_mean = np.mean([-6,-8])
        e_distance_mean = np.mean([-18,-21])
        assert average_lines_in_cluster(cluster, angles, distance) == (e_angle_mean, e_distance_mean)

    def test_empty_cluster():
        with pytest.raises(IndexError):
            angles = np.array([2,4,6,8])
            distance = np.array([12,15,18,21])
            cluster = []
            average_lines_in_cluster(cluster, angles, distance)

    def test_single_element_cluster():
            angles = np.array([2,4,6,8])
            distance = np.array([12,15,18,21])
            cluster = [1]
            assert average_lines_in_cluster(cluster, angles, distance) == (4, 15)
    

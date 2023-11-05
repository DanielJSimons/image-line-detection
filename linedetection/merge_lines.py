import numpy as np

def are_lines_close(angle1, dist1, angle2, dist2, angle_threshold, dist_threshold):
    if angle_threshold == 0 or dist_threshold == 0:
        raise ValueError("Threshold values must be greater than zero.")
    return abs(angle1 - angle2) < angle_threshold and abs(dist1 - dist2) < dist_threshold


def cluster_lines(angles, dists, angle_threshold, dist_threshold):
    clusters = []
    visited = set()
    
    for i in range(len(angles)):
        if i not in visited:
            current_cluster = [i]
            for j in range(i+1, len(angles)):
                if j not in visited and are_lines_close(angles[i], dists[i], angles[j], dists[j], angle_threshold, dist_threshold):
                    current_cluster.append(j)
            visited.update(current_cluster)
            clusters.append(current_cluster)
    return clusters

def average_lines_in_cluster(cluster, angles, dists):
    return np.mean([angles[i] for i in cluster]), np.mean([dists[i] for i in cluster])
import numpy as np

def intersection_points(angle, dist, img_shape):
    y_max, x_max = img_shape
    intersections = []

    # Given y, compute x. (i.e., y = mx + c => x = (y - c) / m)
    m = -np.cos(angle) / np.sin(angle)  # the negative sign accounts for the inverted y-axis in image coordinates
    c = dist / np.sin(angle)
    
    # Boundaries of the image
    x_values_at_y_limits = [(0 - c) / m, (y_max - c) / m]
    y_values_at_x_limits = [m * 0 + c, m * x_max + c]
    
    # Check which values are within the image dimensions
    if 0 <= x_values_at_y_limits[0] <= x_max:
        intersections.append((x_values_at_y_limits[0], 0))
    if 0 <= x_values_at_y_limits[1] <= x_max:
        intersections.append((x_values_at_y_limits[1], y_max))
    if 0 <= y_values_at_x_limits[0] <= y_max:
        intersections.append((0, y_values_at_x_limits[0]))
    if 0 <= y_values_at_x_limits[1] <= y_max:
        intersections.append((x_max, y_values_at_x_limits[1]))

    # Sort intersections based on y-values
    intersections = sorted(intersections, key=lambda k: k[1])

    if len(intersections) >= 2:
        return intersections[0][0], intersections[0][1], intersections[1][0], intersections[1][1]
    else:
        return None, None, None, None
    
def is_line_valid(x0, y0, x1, y1, edge_img, min_length):
    # Generate points along the line
    num_points = int(1.5 * np.hypot(x1-x0, y1-y0))
    x_values = np.linspace(x0, x1, num_points)
    y_values = np.linspace(y0, y1, num_points)
    
    height, width = edge_img.shape
    on_edge_count = 0
    for x, y in zip(x_values, y_values):
        xi, yi = int(x), int(y)
        if 0 <= xi < width and 0 <= yi < height:  # Check if coordinates are within image boundaries
            if edge_img[yi, xi]:
                on_edge_count += 1
                if on_edge_count * np.hypot(x1-x0, y1-y0) / num_points >= min_length:
                    return True
            else:
                on_edge_count = 0  # Reset count if non-edge point found
        else:
            on_edge_count = 0  # Reset count if point is outside image boundaries

    return False
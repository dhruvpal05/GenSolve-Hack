import numpy as np
import cv2

def detect_straight_lines(points, tolerance=1e-2):
    if len(points) < 2:
        return None

    # Fit a line using least squares
    [vx, vy, x, y] = cv2.fitLine(points.astype(np.float32), cv2.DIST_L2, 0, 0.01, 0.01)
    line_start = np.array([x - vx * 1000, y - vy * 1000]).flatten()
    line_end = np.array([x + vx * 1000, y + vy * 1000]).flatten()
    
    # Normalize line vector
    line_vec = np.array([vx, vy]).flatten()
    line_vec /= np.linalg.norm(line_vec)
    
    # Vector from line start to each point
    points = points.astype(np.float32)
    point_vec = np.subtract(points, line_start)
    
    # Calculate the perpendicular distance from points to the line
    dists = np.abs(np.cross(np.repeat(line_vec.reshape(1, -1), len(points), axis=0), point_vec))

    if np.max(dists) < tolerance:
        return np.array([line_start, line_end])
    return None

def fit_circle(points): 
    if len(points) < 3:
        return None

    # Use OpenCV to fit a circle to the points
    (x, y), radius = cv2.minEnclosingCircle(points.astype(np.float32))
    center = np.array([x, y])
    return center, radius

def detect_circle(points, tolerance=1e-2):
    circle = fit_circle(points)
    if circle is not None:
        center, radius = circle
        dists = np.abs(np.linalg.norm(points - center, axis=1) - radius)
        if np.max(dists) < tolerance:
            angles = np.linspace(0, 2 * np.pi, len(points), endpoint=False)
            circle_points = np.array([center + radius * np.array([np.cos(a), np.sin(a)]) for a in angles])
            return circle_points
    return None

def detect_ellipse(points, tolerance=1e-2):
    if len(points) < 5:
        return None

    # Fit an ellipse using OpenCV
    ellipse = cv2.fitEllipse(points.astype(np.float32))
    return ellipse

def detect_rectangle(points, tolerance=1e-2):
    rect = cv2.minAreaRect(points.astype(np.float32))
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box

def detect_rounded_rectangle(points, tolerance=1e-2):
    # Detect a rounded rectangle by fitting a rectangle and checking the corners
    rect = detect_rectangle(points)
    if rect is None:
        return None
    
    # Check if corners are rounded
    corner_radii = []
    for i in range(len(rect)):
        p1 = rect[i]
        p2 = rect[(i + 1) % len(rect)]
        p3 = rect[(i + 2) % len(rect)]
        vec1 = p2 - p1
        vec2 = p3 - p2
        angle = np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        corner_radii.append(angle)
    
    if np.all(np.array(corner_radii) > (np.pi / 2) - tolerance):
        return rect
    return None

def detect_regular_polygon(points, tolerance=1e-2):
    # Approximate the contour with accuracy proportional to the tolerance
    epsilon = tolerance * cv2.arcLength(points, True)
    approx = cv2.approxPolyDP(points, epsilon, True)
    if len(approx) >= 3:  # A valid polygon has at least 3 points
        return approx
    return None

def detect_star_shape(points, tolerance=1e-2):
    # Placeholder for star shape detection, usually more complex
    pass

def regularize_curves(points):
    shapes = {}

    straight_line = detect_straight_lines(points)
    if straight_line is not None:
        shapes['straight_line'] = straight_line
        return shapes

    circle = detect_circle(points)
    if circle is not None:
        shapes['circle'] = circle
        return shapes

    ellipse = detect_ellipse(points)
    if ellipse is not None:
        shapes['ellipse'] = ellipse
        return shapes

    rectangle = detect_rectangle(points)
    if rectangle is not None:
        shapes['rectangle'] = rectangle
        return shapes

    rounded_rectangle = detect_rounded_rectangle(points)
    if rounded_rectangle is not None:
        shapes['rounded_rectangle'] = rounded_rectangle
        return shapes

    regular_polygon = detect_regular_polygon(points)
    if regular_polygon is not None:
        shapes['regular_polygon'] = regular_polygon
        return shapes

    star_shape = detect_star_shape(points)
    if star_shape is not None:
        shapes['star_shape'] = star_shape
        return shapes

    return shapes



# import numpy as np
# import cv2

# def smooth_points(points, kernel_size=5):
#     smoothed = cv2.GaussianBlur(points, (kernel_size, kernel_size), 0)
#     return smoothed

# def detect_straight_lines(points, tolerance=5.0):
#     if len(points) < 2:
#         return None

#     # Fit a line using least squares
#     [vx, vy, x, y] = cv2.fitLine(points.astype(np.float32), cv2.DIST_L2, 0, 0.01, 0.01)
#     line_start = np.array([x - vx * 1000, y - vy * 1000]).flatten()
#     line_end = np.array([x + vx * 1000, y + vy * 1000]).flatten()
    
#     # Normalize line vector
#     line_vec = np.array([vx, vy]).flatten()
#     line_vec /= np.linalg.norm(line_vec)
    
#     # Vector from line start to each point
#     points = points.astype(np.float32)
#     point_vec = np.subtract(points, line_start)
    
#     # Calculate the perpendicular distance from points to the line
#     dists = np.abs(np.cross(np.repeat(line_vec.reshape(1, -1), len(points), axis=0), point_vec))

#     if np.max(dists) < tolerance:
#         return np.array([line_start, line_end])
#     return None

# def fit_circle(points): 
#     if len(points) < 3:
#         return None

#     # Use OpenCV to fit a circle to the points
#     (x, y), radius = cv2.minEnclosingCircle(points.astype(np.float32))
#     center = np.array([x, y])
#     return center, radius

# def detect_circle(points, tolerance=5.0):
#     circle = fit_circle(points)
#     if circle is not None:
#         center, radius = circle
#         dists = np.abs(np.linalg.norm(points - center, axis=1) - radius)
#         if np.max(dists) < tolerance:
#             angles = np.linspace(0, 2 * np.pi, len(points), endpoint=False)
#             circle_points = np.array([center + radius * np.array([np.cos(a), np.sin(a)]) for a in angles])
#             return circle_points
#     return None

# def detect_ellipse(points, tolerance=5.0):
#     if len(points) < 5:
#         return None

#     # Fit an ellipse using OpenCV
#     ellipse = cv2.fitEllipse(points.astype(np.float32))
#     return ellipse

# def detect_rectangle(points, tolerance=5.0):
#     rect = cv2.minAreaRect(points.astype(np.float32))
#     box = cv2.boxPoints(rect)
#     box = np.int0(box)
#     return box

# def detect_rounded_rectangle(points, tolerance=5.0):
#     # Detect a rounded rectangle by fitting a rectangle and checking the corners
#     rect = detect_rectangle(points)
#     if rect is None:
#         return None
    
#     # Check if corners are rounded
#     corner_radii = []
#     for i in range(len(rect)):
#         p1 = rect[i]
#         p2 = rect[(i + 1) % len(rect)]
#         p3 = rect[(i + 2) % len(rect)]
#         vec1 = p2 - p1
#         vec2 = p3 - p2
#         angle = np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
#         corner_radii.append(angle)
    
#     if np.all(np.array(corner_radii) > (np.pi / 2) - tolerance):
#         return rect
#     return None

# def detect_regular_polygon(points, tolerance=5.0):
#     # Approximate the contour with accuracy proportional to the tolerance
#     epsilon = tolerance * cv2.arcLength(points, True)
#     approx = cv2.approxPolyDP(points, epsilon, True)
#     if len(approx) >= 3:  # A valid polygon has at least 3 points
#         return approx
#     return None

# def detect_star_shape(points, tolerance=5.0):
#     # Placeholder for star shape detection, usually more complex
#     pass

# def regularize_curves(points):
#     shapes = {}

#     # Smooth points to handle freehand drawing noise
#     points = smooth_points(points)

#     straight_line = detect_straight_lines(points)
#     if straight_line is not None:
#         shapes['straight_line'] = straight_line
#         return shapes

#     circle = detect_circle(points)
#     if circle is not None:
#         shapes['circle'] = circle
#         return shapes

#     ellipse = detect_ellipse(points)
#     if ellipse is not None:
#         shapes['ellipse'] = ellipse
#         return shapes

#     rectangle = detect_rectangle(points)
#     if rectangle is not None:
#         shapes['rectangle'] = rectangle
#         return shapes

#     rounded_rectangle = detect_rounded_rectangle(points)
#     if rounded_rectangle is not None:
#         shapes['rounded_rectangle'] = rounded_rectangle
#         return shapes

#     regular_polygon = detect_regular_polygon(points)
#     if regular_polygon is not None:
#         shapes['regular_polygon'] = regular_polygon
#         return shapes

#     star_shape = detect_star_shape(points)
#     if star_shape is not None:
#         shapes['star_shape'] = star_shape
#         return shapes

#     return shapes

# # Example Usage:
# # points = np.array([...])  # Replace with the actual points from a freehand drawing
# # shapes = regularize_curves(points)
# # print(shapes)

import numpy as np
import cv2

def complete_curve(curve, tolerance=1e-2):
    # Use OpenCV to find the convex hull of the points
    hull = cv2.convexHull(curve.astype(np.float32))
    if len(hull) > 2:
        return hull.reshape(-1, 2)
    return curve

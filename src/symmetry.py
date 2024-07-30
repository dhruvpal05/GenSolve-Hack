# import numpy as np

# def find_symmetry_line(points):
#     centroid = np.mean(points, axis=0)
#     centered_points = points - centroid
#     covariance_matrix = np.cov(centered_points, rowvar=False)
#     eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
#     symmetry_axis = eigenvectors[:, np.argmin(eigenvalues)]
#     return symmetry_axis, centroid

import numpy as np
import cv2

def find_symmetry_line(points):
    # Convert points to float32 for PCA
    points = np.array(points, dtype=np.float32)
    
    # Calculate the mean (centroid) of the points
    mean, eigenvectors = cv2.PCACompute(points, mean=None)
    
    # The symmetry axis is the eigenvector corresponding to the smallest eigenvalue
    symmetry_axis = eigenvectors[0]
    
    # The mean is already computed as the centroid
    centroid = mean[0]
    
    return symmetry_axis, centroid

# Example usage
# points = np.array([
#     [1, 2],
#     [2, 3],
#     [3, 4],
#     [4, 5],
#     [5, 6]
# ])

# symmetry_axis, centroid = find_symmetry_line(points)
# print(f'Symmetry Axis: {symmetry_axis}')
# print(f'Centroid: {centroid}')



# import numpy as np

# def find_symmetry_line(points):
#     # Check for reflection symmetry
#     midpoint = np.mean(points, axis=0)
#     mirrored_points = points[::-1]
#     symmetry = np.allclose(points, mirrored_points, atol=1e-2)
#     return symmetry

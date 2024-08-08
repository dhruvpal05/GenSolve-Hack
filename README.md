# GenSolve-Hack

# Shape Detection and Symmetry Analysis

## Overview

This project provides a Python-based solution for detecting various shapes in images and analyzing their symmetry. The script processes images to identify shapes such as circles, stars, rectangles, and ellipses. It also checks for reflectional and rotational symmetry within these shapes. The results are visualized and saved in image format.

## Features

- **Shape Detection**: Detects circles, stars, rectangles, rounded rectangles, ellipses, and polygons in images.
- **Symmetry Detection**: Analyzes shapes for reflectional and rotational symmetry.
- **Visualization**: Overlays detected shapes and highlights symmetric shapes on the original image.
- **Customizable**: Users can specify which shapes to detect.

## Installation

To run this script, you'll need Python 3.7+ and a few Python packages. Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage

### Input

- **CSV File**: The script processes images from CSV files. Each CSV file contains coordinates representing shapes.
- **Shapes to Detect**: Users can specify the types of shapes they want to detect by modifying the `shapes_to_detect` list in the script.

### Output

- **Detected Shapes**: The script outputs an image with the detected shapes overlaid.
- **Symmetry Analysis**: Symmetric shapes are highlighted in red.
- **Saved Image**: The final processed image is saved as `detected_shapes_with_symmetry.png`.

### Example

```python
# Example usage
shapes_to_detect = ['circles', 'stars', 'rectangles']  # Specify the shapes you want to detect
csv_image, original_paths = parse_csv_with_read_csv('isolated.csv')
preprocessed_image = preprocess_image(csv_image)
shapes = detect_shapes(preprocessed_image, shapes_to_detect)
symmetric_shapes = detect_symmetry(shapes)
plot_shapes(preprocessed_image, shapes)
final_image = overlay_detected_shapes(preprocessed_image, original_paths, shapes, symmetric_shapes)

# Display the final image
final_image.save("detected_shapes_with_symmetry.png")
final_image.show()
```

### Functions

- `read_csv(csv_path)`: Reads the CSV file and organizes data into paths.
- `parse_csv_with_read_csv(csv_path, scale=5)`: Parses the CSV data and scales the coordinates.
- `preprocess_image(image)`: Applies Gaussian blur to the image.
- `detect_shapes(image, shapes_to_detect)`: Detects specified shapes in the image.
- `plot_shapes(image, shapes)`: Plots the detected shapes on the image.
- `is_reflectionally_symmetric(points)`: Checks if a shape is reflectionally symmetric.
- `is_rotationally_symmetric(points)`: Checks if a shape is rotationally symmetric.
- `detect_symmetry(shapes)`: Detects symmetry for the detected shapes.
- `overlay_detected_shapes(original_image, original_paths, shapes, symmetric_shapes)`: Overlays detected shapes and highlights symmetric shapes on the image.

## Files

- **`Shape_detection_and_Symmetry.py`**: The main script for detecting and analyzing shapes and their symmetry.
- **`requirements.txt`**: Lists all required Python packages.
- **`isolated.csv`**: Example CSV file used for shape detection (optional).

## Future Work

- **Enhance Symmetry Detection**: Improve the algorithms for detecting symmetry, especially for complex polygons.
- **SVG Output**: Add functionality to save the final result in SVG format.
- **Performance Optimization**: Optimize the script for processing larger images more efficiently.



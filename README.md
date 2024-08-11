<p align="center">
  <strong><h1 style="font-size: 60px;" align="center">GenSolve-Hack</h1></strong>
</p>

## Problem Statement 

Our mission is to identify, regularize, and beautify curves in 2D Euclidean
space. We’ll start by focusing on closed curves and progressively work with more com-
plex shapes. This project will also cover symmetry and curve completion techniques.

## Solution Summary 

### Task-1-and-2
#### <a href="https://github.com/dhruvpal05/GenSolve-Hack/blob/main/Task-1-and-2/README.md">Go to Detailed Docs</a>
The script takes CSV data representing paths and converts them into an image with geometric shapes drawn. It then preprocesses the image to enhance shape detection using edge detection and contour finding. Various shapes, including lines, rectangles, circles, ellipses, and polygons, are detected and analyzed for symmetry properties (both reflectional and rotational). The detected shapes and their symmetries are highlighted and overlaid on the original image, providing a visual representation of the shapes and their symmetrical characteristics. This output is saved as an image file for review and further analysis.

### Task-3
#### <a href="https://github.com/dhruvpal05/GenSolve-Hack/blob/main/Task-3/README.md">Go to Detailed Docs</a>
#### Color Segmentation and Mask Completion

This script extracts unique non-white colors from an image, segments the image based on these colors, and refines the masks using morphological operations. It then combines the processed masks into a single image and saves it.

#### Occlusion Detection and Completion

This script processes a grayscale image to create a binary mask, applies morphological operations to complete the mask, and then resizes and combines the images to show the mask completion process. It saves and displays the final result.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dhruvpal05/GenSolve-Hack
   cd GenSolve-Hack
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Go to the respective Task's detailed docs to continue**

   <a font-size="10px" href="https://github.com/dhruvpal05/GenSolve-Hack/blob/main/Task-1-and-2/README.md">Detailed Docs for Task 1 & 2</a>

   <a href="https://github.com/dhruvpal05/GenSolve-Hack/blob/main/Task-3/README.md">Detailed Docs for Task 3</a>

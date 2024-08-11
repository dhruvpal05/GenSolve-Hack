<p align="center">
  <strong><span style="font-size: 24px;">GenSolve-Hack</span></strong>
</p>


## Problem Statement 

Ideally we want a end to end process where we take a PNG
(raster) image of a line art and output a set of curves, where the curves are defined as
a connected sequence of cubic Bézier curves.
However to begin, we are allowed to make the following simplification. Instead of
PNG as input, we will present line art in the form of polylines, which is defined as sequence
of points. To be precise, let a path be a finite sequence of point { pi }1≤i<=n from R2 , and
P be the set of all paths in R2 . The input to our problem is finite subset of paths from P .
The expected output is another set of paths with the necessary properties of regularization,
symmetry and completeness as defined in next sections.
For visualization, we may use SVG format that can be rendered on a browser, and
the output curve can be in the form of cubic Bézier instead of polylines. The principal
challenge is divided in the following sections.

## Solution Summary 

### Task-1-and-2
The script takes CSV data representing paths and converts them into an image with geometric shapes drawn. It then preprocesses the image to enhance shape detection using edge detection and contour finding. Various shapes, including lines, rectangles, circles, ellipses, and polygons, are detected and analyzed for symmetry properties (both reflectional and rotational). The detected shapes and their symmetries are highlighted and overlaid on the original image, providing a visual representation of the shapes and their symmetrical characteristics. This output is saved as an image file for review and further analysis.

### Task-3

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
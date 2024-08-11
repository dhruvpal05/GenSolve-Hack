

---

# Image Segmentation and Mask Concatenation

This script processes an image by automatically detecting unique non-white colors, segmenting the image based on these colors, and then concatenating the masks of these segmented regions side by side. The final output is saved as an image file.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Explanation of Key Steps](#explanation-of-key-steps)
- [Example Output](#example-output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you run this script, ensure you have the following installed:

- Python 3.x
- `numpy`
- `opencv-python`
- `matplotlib`
- `shapely`

## Installation

To install the necessary Python libraries, you can use the following pip command:

```bash
pip install numpy opencv-python matplotlib shapely
```

## Usage

1. **Place your image**: Ensure the image you want to process is placed in the same directory as the script or provide the correct path to the image.

2. **Run the script**: You can run the script with the following command:

   ```bash
   python script_name.py
   ```

   Replace `script_name.py` with the actual name of your script file.

3. **Output**: The script will generate and save an image called `combined_masks.png` in the same directory. This image will contain the concatenated masks of the segmented regions side by side.

## Explanation of Key Steps

1. **Image Loading**: The script loads the image using OpenCV. The image is expected to be in the BGR format, as that's how OpenCV reads images by default.

2. **Unique Color Extraction**: The script converts the image to RGB and extracts unique non-white colors. These colors are then converted to the HSV color space.

3. **Color Range Formatting**: For each detected color in HSV format, a range is generated for segmentation. This range is used to create masks for each color.

4. **Segmentation**: The image is segmented based on the HSV ranges. Masks are created for each detected color.

5. **Mask Completion**: The script completes the masks using morphological operations and convex hulls to ensure that the regions are fully enclosed and contiguous.

6. **Mask Concatenation**: Two masks are concatenated side by side. The script assumes there are at least two masks; otherwise, it will raise an error.

7. **Output**: The concatenated image is saved and optionally displayed.

## Example Output

Here is an example of what the output image might look like:

![Combined Masks](path_to_combined_masks.png)

> Replace `path_to_combined_masks.png` with the actual path to the output image.

## Troubleshooting

- **Image Not Found**: Ensure that the image path provided in the script is correct and that the image exists in the specified location.

- **Not Enough Masks**: If the script raises an error about not having enough masks, make sure that the image contains at least two distinct non-white colors.

- **Color Detection Issues**: If the script is not detecting the colors correctly, consider adjusting the `white_threshold` or the range used for color segmentation.

## Contributing

Contributions to this project are welcome. If you find any bugs or have suggestions for improvements, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

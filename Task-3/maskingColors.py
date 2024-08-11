import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# Parameters
white_threshold = 240  # Adjust the threshold as needed

def load_image(image_path):
    """Load an image."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path '{image_path}' could not be loaded.")
    return image

def extract_unique_colors(image_rgb):
    """Extract unique non-white colors from the image and convert them to HSV."""
    # Reshape the image to be a list of pixels
    pixels = image_rgb.reshape(-1, 3)

    # Filter out white or near-white pixels
    filtered_pixels = pixels[np.all(pixels < [white_threshold, white_threshold, white_threshold], axis=1)]

    # Remove duplicate colors
    unique_colors = np.unique(filtered_pixels, axis=0)

    # Convert unique colors from RGB to HSV
    unique_colors_hsv = cv2.cvtColor(unique_colors.reshape(-1, 1, 3), cv2.COLOR_RGB2HSV).reshape(-1, 3)
    
    return unique_colors_hsv

def format_color_ranges(unique_colors_hsv):
    """Format the HSV values into tuples for color segmentation."""
    color_ranges = []
    for hsv_value in unique_colors_hsv:
        lower_bound = np.clip(hsv_value - [10, 40, 40], 0, 255)
        upper_bound = np.clip(hsv_value + [10, 40, 40], 0, 255)
        color_ranges.append((tuple(lower_bound), tuple(upper_bound)))
    return color_ranges

def segment_by_color(image, color_ranges):
    """Segment the image by color using provided HSV ranges."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    masks = []
    
    for lower, upper in color_ranges:
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        masks.append(mask)
    
    return masks

def complete_mask(mask):
    """Complete incomplete masks using morphological operations and convex hull."""
    # Define kernel for morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    
    # Fill holes in the mask (closing operation)
    mask_filled = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Optional: Further improve mask by dilation to close small gaps
    mask_dilated = cv2.dilate(mask_filled, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(mask_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create an empty mask to draw the convex hull
    convex_hull_mask = np.zeros_like(mask)
    
    for contour in contours:
        # Compute the convex hull of the contour
        hull = cv2.convexHull(contour)
        cv2.drawContours(convex_hull_mask, [hull], 0, 255, -1)  # Draw filled hull
    
    # Combine the dilated mask and convex hull mask
    combined_mask = cv2.bitwise_or(mask_dilated, convex_hull_mask)
    
    return combined_mask

def concatenate_masks(mask1, mask2):
    """Concatenate two masks side by side."""
    # Ensure both masks have the same height
    height = max(mask1.shape[0], mask2.shape[0])
    width1 = mask1.shape[1]
    width2 = mask2.shape[1]
    
    # Resize masks to the same height
    if mask1.shape[0] != height:
        mask1 = cv2.resize(mask1, (width1, height))
    if mask2.shape[0] != height:
        mask2 = cv2.resize(mask2, (width2, height))
    
    # Concatenate masks horizontally
    combined = np.hstack((mask1, mask2))
    return combined

def save_image(image, filename):
    """Save the image to the specified file in the output folder."""
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)
    full_path = os.path.join(output_folder, filename)
    cv2.imwrite(full_path, image)
    print(f"Image saved as {full_path}")

def main(image_path):
    # Step 1: Load the image
    image = load_image(image_path)
    
    # Convert the image from BGR to RGB (since OpenCV loads in BGR format)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Step 2: Extract unique non-white colors and convert to HSV
    unique_colors_hsv = extract_unique_colors(image_rgb)
    
    # Step 3: Format the HSV values into tuples for color segmentation
    color_ranges = format_color_ranges(unique_colors_hsv)
    
    # Step 4: Segment the image by color using the extracted ranges
    masks = segment_by_color(image, color_ranges)
    
    # Ensure we have at least two masks
    if len(masks) < 2:
        raise ValueError("Expected at least two masks for concatenation.")
    
    # Step 5: Complete the masks
    mask1 = complete_mask(masks[0])
    mask2 = complete_mask(masks[1])
    
    # Step 6: Concatenate the masks side by side
    combined_image = concatenate_masks(mask1, mask2)
    
    # Extract the base name of the image file without extension
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    output_filename = f"mask_{base_name}.png"
    save_image(combined_image, output_filename)
    
    # Step 7: Display the result using plt.show
    plt.imshow(combined_image, cmap='gray')
    plt.title('Combined Masks')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Example usage
    image_path = './problems/occlusion1_rec.png'  # Use the uploaded image path
    main(image_path)

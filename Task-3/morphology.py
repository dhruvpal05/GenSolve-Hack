import cv2
import numpy as np
import os

def detect_and_complete_occlusion(img_path):
    # Load the image as grayscale
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    print("Print any key to interrupt")

    if image is None:
        print("Error loading image. Please check the file path and file format.")
        return None

    # Threshold the image to create a binary mask
    _, binary_mask = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Define the kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)

    # Perform morphological operations
    eroded_mask = cv2.erode(binary_mask, kernel, iterations=1)
    dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=3)
    closing_kernel = np.ones((15, 15), np.uint8)
    closed_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, closing_kernel)
    completed_mask = cv2.dilate(closed_mask, kernel, iterations=2)
    completed_image = cv2.bitwise_and(image, image, mask=completed_mask)

    # Resize all images to the same height for uniformity
    height = max(image.shape[0], binary_mask.shape[0], eroded_mask.shape[0], dilated_mask.shape[0],
                  closed_mask.shape[0], completed_mask.shape[0], completed_image.shape[0])

    def resize_to_height(img, height):
        """Resize image to a specific height while maintaining aspect ratio."""
        ratio = height / img.shape[0]
        new_width = int(img.shape[1] * ratio)
        return cv2.resize(img, (new_width, height))

    image_resized = resize_to_height(image, height)
    binary_mask_resized = resize_to_height(binary_mask, height)
    eroded_mask_resized = resize_to_height(eroded_mask, height)
    dilated_mask_resized = resize_to_height(dilated_mask, height)
    closed_mask_resized = resize_to_height(closed_mask, height)
    completed_mask_resized = resize_to_height(completed_mask, height)
    completed_image_resized = resize_to_height(completed_image, height)

    # Concatenate all images horizontally
    combined_image = np.hstack([image_resized, binary_mask_resized, eroded_mask_resized,
                                dilated_mask_resized, closed_mask_resized, completed_mask_resized,
                                completed_image_resized])

    # Create the output directory if it does not exist
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)

    # Create the output file name
    base_name = os.path.basename(img_path)
    name, _ = os.path.splitext(base_name)
    output_filename = f'morphed_{name}.png'
    output_path = os.path.join(output_folder, output_filename)

    # Save the combined image
    cv2.imwrite(output_path, combined_image)
    print(f"Combined image saved as {output_path}")

    # Display the combined image
    cv2.imshow('Results', combined_image)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

    return completed_image

# Example usage:
if __name__ == "__main__":
    img_path = './problems/occlusion1_rec.png'
    detect_and_complete_occlusion(img_path)

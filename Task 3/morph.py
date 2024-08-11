import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_and_complete_occlusion(img_path):
    """
    Detects occlusions in the image and completes the occluded parts using morphological operations.

    Args:
    img_path (str): The file path to the grayscale image.

    Returns:
    completed_image (numpy.ndarray): The image with the occluded parts completed.
    """

    # Load the image as grayscale
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Error loading image. Please check the file path and file format.")
        return None

    # Threshold the image to create a binary mask
    _, binary_mask = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Define the kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)

    # Perform morphological operations
    # Erosion: Removes small-scale noise
    eroded_mask = cv2.erode(binary_mask, kernel, iterations=1)

    # Dilation: Fills small holes and gaps
    dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=3)

    # Fill the occluded areas using morphological closing
    closing_kernel = np.ones((15, 15), np.uint8)  # Larger kernel for closing
    closed_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, closing_kernel)

    # Further dilation after closing to expand filled areas
    completed_mask = cv2.dilate(closed_mask, kernel, iterations=2)

    # Apply the completed mask to the original image
    completed_image = cv2.bitwise_and(image, image, mask=completed_mask)

    # Show the results
    plt.figure(figsize=(14, 8))

    plt.subplot(2, 4, 1)
    plt.title("Original Image")
    plt.imshow(image, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 2)
    plt.title("Binary Mask")
    plt.imshow(binary_mask, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 3)
    plt.title("Eroded Mask")
    plt.imshow(eroded_mask, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 4)
    plt.title("Dilated Mask")
    plt.imshow(dilated_mask, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 5)
    plt.title("Closed Mask")
    plt.imshow(closed_mask, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 6)
    plt.title("Completed Mask")
    plt.imshow(completed_mask, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 7)
    plt.title("Completed Image")
    plt.imshow(completed_image, cmap='gray')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Optionally, save the results
    cv2.imwrite('eroded_mask.png', eroded_mask)
    cv2.imwrite('dilated_mask.png', dilated_mask)
    cv2.imwrite('closed_mask.png', closed_mask)
    cv2.imwrite('completed_mask.png', completed_mask)
    cv2.imwrite('completed_image.png', completed_image)

    return completed_image

# Example usage:
if __name__ == "__main__":
    img_path = input("Enter the path to the image: ")
    detect_and_complete_occlusion(img_path)

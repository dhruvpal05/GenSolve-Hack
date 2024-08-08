#FINAL SCRIPT WITH SYMMETRY
import numpy as np
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def read_csv(csv_path):
    """Read CSV file and organize data into paths."""
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def parse_csv_with_read_csv(csv_path, scale=5):
    path_XYs = read_csv(csv_path)

    width, height = 500 * scale, 500 * scale
    image = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(image)

    original_paths = []

    for XYs in path_XYs:
        path_points = []
        for XY in XYs:
            points = [(x * scale, y * scale) for x, y in XY]
            draw.line(points, fill=0, width=1)
            path_points.append(points)
        original_paths.append(path_points)

    return np.array(image), original_paths

def preprocess_image(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred

def detect_shapes(image, shapes_to_detect):
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    shapes = {shape: [] for shape in shapes_to_detect}

    for contour in contours:
        if cv2.contourArea(contour) < 100:
            continue

        if 'lines' in shapes_to_detect:
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=100, maxLineGap=10)
            if lines is not None:
                for line in lines:
                    for x1, y1, x2, y2 in line:
                        shapes['lines'].append(((x1, y1), (x2, y2)))

        if 'rectangles' in shapes_to_detect or 'rounded_rectangles' in shapes_to_detect:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:
                shapes['rectangles'].append(approx)
                if 'rounded_rectangles' in shapes_to_detect:
                    hull = cv2.convexHull(approx)
                    hull_area = cv2.contourArea(hull)
                    contour_area = cv2.contourArea(contour)
                    area_ratio = contour_area / hull_area
                    if area_ratio < 0.9:
                        shapes['rounded_rectangles'].append(approx)

        if 'stars' in shapes_to_detect:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) >= 5:
                hull = cv2.convexHull(approx)
                hull_area = cv2.contourArea(hull)
                contour_area = cv2.contourArea(contour)
                area_ratio = contour_area / hull_area
                if area_ratio < 0.8:
                    shapes['stars'].append(approx)

        min_contour_area = 350000  # Adjust this value based on your requirements

        if 'circles' in shapes_to_detect:
        # Circle detection using contour circularity
            area = cv2.contourArea(contour)
            if area < min_contour_area:
                continue  # Skip contours that are too small to be considered circles

            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue

            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if 0.7 < circularity < 1.2:  # Adjust the range for circularity as needed
                (x, y), radius = cv2.minEnclosingCircle(contour)
                shapes['circles'].append((int(x), int(y), int(radius)))

        if 'ellipses' in shapes_to_detect:
            if len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                shapes['ellipses'].append(ellipse)

        if 'polygons' in shapes_to_detect:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) >= 5:
                polygon = np.array(approx).reshape(-1, 2)
                num_sides = len(polygon)
                angles = []
                for i in range(num_sides):
                    p1, p2, p3 = polygon[i], polygon[(i + 1) % num_sides], polygon[(i + 2) % num_sides]
                    angle = np.arccos(np.dot(p2 - p1, p2 - p3) / (np.linalg.norm(p2 - p1) * np.linalg.norm(p2 - p3)))
                    angles.append(angle)
                avg_angle = np.mean(angles)
                if np.allclose(angles, avg_angle, atol=0.1):
                    shapes['polygons'].append(approx)
    print("Detected shapes:")
    # can be used to print the coordinates of the shapes detected (or center, radius in case of circle)
    # for shape_type, shape_list in shapes.items():
    #     if shape_list:
    #         print(f"- {shape_type.capitalize()}: {len(shape_list)} detected")
    #         for i, shape in enumerate(shape_list, 1):
    #             print(f"  {i}. {shape}")
    for shape_type, shape_list in shapes.items():
        if shape_list:
            print(f"- {shape_type.capitalize()}")                   

    return shapes

def plot_shapes(original_image, processed_image, shapes):
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # Show the original image
    axes[0].imshow(original_image, cmap='gray')
    axes[0].set_title("Original Image")
    axes[0].axis("off")

    # Show the processed image with detected shapes
    axes[1].imshow(processed_image, cmap='gray')
    axes[1].set_title("Detected Shapes")
    axes[1].axis("off")

    if 'lines' in shapes:
        for line in shapes['lines']:
            (x1, y1), (x2, y2) = line
            axes[1].plot([x1, x2], [y1, y2], 'b-', linewidth=2)

    if 'circles' in shapes:
        for circle in shapes['circles']:
            cx, cy, r = circle
            circle_patch = plt.Circle((cx, cy), r, color='g', fill=False, linewidth=2)
            axes[1].add_patch(circle_patch)

    if 'ellipses' in shapes:
        for ellipse in shapes['ellipses']:
            center, axes_length, angle = ellipse
            ellipse_patch = Ellipse(center, axes_length[0], axes_length[1], angle=angle, color='r', fill=False, linewidth=2)
            axes[1].add_patch(ellipse_patch)

    if 'rectangles' in shapes:
        for rect in shapes['rectangles']:
            rect = np.array(rect)
            axes[1].plot(rect[:, 0, 0], rect[:, 0, 1], 'c-', linewidth=2)
            axes[1].plot([rect[-1, 0, 0], rect[0, 0, 0]], [rect[-1, 0, 1], rect[0, 0, 1]], 'c-', linewidth=2)

    if 'rounded_rectangles' in shapes:
        for rounded_rect in shapes['rounded_rectangles']:
            rounded_rect = np.array(rounded_rect)
            axes[1].plot(rounded_rect[:, 0, 0], rounded_rect[:, 0, 1], 'm-', linewidth=2)
            axes[1].plot([rounded_rect[-1, 0, 0], rounded_rect[0, 0, 0]], [rounded_rect[-1, 0, 1], rounded_rect[0, 0, 1]], 'm-', linewidth=2)

    if 'polygons' in shapes:
        for polygon in shapes['polygons']:
            polygon = np.array(polygon)
            axes[1].plot(polygon[:, 0, 0], polygon[:, 0, 1], 'y-', linewidth=2)
            axes[1].plot([polygon[-1, 0, 0], polygon[0, 0, 0]], [polygon[-1, 0, 1], polygon[0, 0, 1]], 'y-', linewidth=2)

    if 'stars' in shapes:
        for star in shapes['stars']:
            star = np.array(star)
            axes[1].plot(star[:, 0, 0], star[:, 0, 1], 'b-', linewidth=2)
            axes[1].plot([star[-1, 0, 0], star[0, 0, 0]], [star[-1, 0, 1], star[0, 0, 1]], 'b-', linewidth=2)

    plt.show()


def is_reflectionally_symmetric(points):
    """Check if the points of a shape are reflectionally symmetric."""
    # Convert points to a numpy array
    points = np.array(points)

    # Check horizontal and vertical symmetry lines
    # For simplicity, this example assumes that the points are ordered
    centroid = np.mean(points, axis=0)
    for angle in [0, np.pi / 2]:
        rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                               [np.sin(angle),  np.cos(angle)]])
        rotated_points = (rot_matrix @ (points - centroid).T).T + centroid
        if np.all(np.isclose(rotated_points, np.flipud(points), atol=1e-2)):
            return True
    return False

def is_rotationally_symmetric(points):
    """Check if the points of a shape are rotationally symmetric."""
    points = np.array(points)
    n = len(points)

    if n < 3:
        return False

    for i in range(n):
        rotated_points = np.roll(points, i, axis=0)
        if np.all(np.isclose(rotated_points, points, atol=1e-2)):
            return True
    return False

def detect_symmetry(shapes):
    """Detect symmetry for the detected shapes and print results."""
    symmetric_shapes = {'reflectional': [], 'rotational': []}

    for shape_type, shape_list in shapes.items():
        for shape in shape_list:
            if shape_type == 'lines':
                # Lines don't typically have symmetry in the same way as shapes.
                continue

            if shape_type in ['circles', 'ellipses']:
                # Skip these shapes for symmetry detection as they are not usually handled this way.
                continue

            # Assuming shape is a list of points in the format [[x, y], [x, y], ...]
            try:
                points = np.array([pt[0] for pt in shape])
            except (TypeError, IndexError) as e:
                print(f"Error processing shape: {e}")
                continue

            has_reflectional_symmetry = is_reflectionally_symmetric(points)
            has_rotational_symmetry = is_rotationally_symmetric(points)

            if has_reflectional_symmetry:
                symmetric_shapes['reflectional'].append(shape)
                print(f"{shape_type.capitalize()} shape with points {points} has reflectional symmetry.")
            if has_rotational_symmetry:
                symmetric_shapes['rotational'].append(shape)
                print(f"{shape_type.capitalize()} shape with points {points} has rotational symmetry.")

    if not symmetric_shapes['reflectional'] and not symmetric_shapes['rotational']:
        print("No shapes with symmetry detected.")

    return symmetric_shapes



def overlay_detected_shapes(original_image, original_paths, shapes, symmetric_shapes):
    if isinstance(original_image, np.ndarray):
        final_image = Image.fromarray(original_image)
    else:
        final_image = original_image.copy()

    if final_image.mode != 'L':
        final_image = final_image.convert('L')
    draw = ImageDraw.Draw(final_image)

    # Draw original paths
    for path_points in original_paths:
        for points in path_points:
            if len(points) > 1:
                draw.line(points, fill=0, width=1)

    # Draw detected shapes
    for shape_type, shape_list in shapes.items():
        if shape_type == 'lines':
            for line in shape_list:
                (x1, y1), (x2, y2) = line
                draw.line([x1, y1, x2, y2], fill=0, width=2)
        elif shape_type == 'circles':
            for circle in shape_list:
                cx, cy, r = circle
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=0, width=2)
        elif shape_type == 'ellipses':
            for ellipse in shape_list:
                center, axes, angle = ellipse
                draw.ellipse([
                    center[0] - axes[0], center[1] - axes[1],
                    center[0] + axes[0], center[1] + axes[1]
                ], outline=0, width=2)
        elif shape_type in ['rectangles', 'rounded_rectangles', 'polygons', 'stars']:
            for shape in shape_list:
                for i in range(len(shape)):
                    p1 = tuple(shape[i, 0])
                    p2 = tuple(shape[(i + 1) % len(shape), 0])
                    draw.line([p1, p2], fill=0, width=2)

    # Highlight symmetric shapes
    for shape_type, shape_list in symmetric_shapes.items():
        for shape in shape_list:
            for i in range(len(shape)):
                p1 = tuple(shape[i, 0])
                p2 = tuple(shape[(i + 1) % len(shape), 0])
                draw.line([p1, p2], fill='red', width=2)

    return final_image

# Example usage
shapes_to_detect = ['circles','stars','rectangles']  # Specify the shapes you want to detect
csv_image, original_paths = parse_csv_with_read_csv('isolated.csv')
preprocessed_image = preprocess_image(csv_image)
shapes = detect_shapes(preprocessed_image, shapes_to_detect)
symmetric_shapes = detect_symmetry(shapes)

# Overlay the detected shapes and symmetries
final_image = overlay_detected_shapes(preprocessed_image, original_paths, shapes, symmetric_shapes)

# Plot original and detected shapes side by side
plot_shapes(csv_image, final_image, shapes)

# Save the final image with detected shapes and symmetry
final_image.save("detected_shapes_with_symmetry.png")
final_image.show()
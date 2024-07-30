# src/main.py

from read_data import read_csv
from visualize import plot
from regularize import regularize_curves
from symmetry import find_symmetry_line
from completion import complete_curve
from utils import polylines2svg
import os
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logging.info("Starting the curve regularization process")

    data_dir = '../data/examples/'
    output_dir = '../data/output/'
    input_files = ['isolated.csv']

    os.makedirs(output_dir, exist_ok=True)

    for input_file in input_files:
        try:
            paths_XYs = read_csv(os.path.join(data_dir, input_file))
            logging.info(f"Input data read successfully for {input_file}")
        except Exception as e:
            logging.error(f"Error reading input data: {e}")
            continue

        try:
            plot(paths_XYs)
            logging.info("Input data visualized successfully")
        except Exception as e:
            logging.error(f"Error visualizing input data: {e}")

        regularized_paths_XYs = []
        for paths in paths_XYs:
            regularized_paths = []
            for points in paths:
                shapes = regularize_curves(points)
                logging.info(f'Detected shapes: {shapes}')
                
                # Calculate symmetry line
                symmetry_axis, centroid = find_symmetry_line(points)
                logging.info(f'Symmetry Axis: {symmetry_axis}, Centroid: {centroid}')
                
                if 'straight_line' in shapes:
                    regularized_paths.append(shapes['straight_line'])
                elif 'circle' in shapes:
                    regularized_paths.append(shapes['circle'])
                else:
                    regularized_paths.append(points)
            regularized_paths_XYs.append(regularized_paths)

        completed_paths_XYs = []
        for paths in regularized_paths_XYs:
            completed_paths = []
            for points in paths:
                completed_curve = complete_curve(points)
                completed_paths.append(completed_curve)
            completed_paths_XYs.append(completed_paths)

        try:
            input_filename_wo_ext = os.path.splitext(input_file)[0]
            svg_filename = f"{input_filename_wo_ext}_sol.svg"
            svg_path = os.path.join(output_dir, svg_filename)
            polylines2svg(completed_paths_XYs, svg_path)
            logging.info(f'Output saved to {svg_path}')
        except Exception as e:
            logging.error(f"Error saving output: {e}")

if __name__ == "__main__":
    main()

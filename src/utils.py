import numpy as np
import svgwrite
import cairosvg

def polylines2svg(paths_XYs, svg_path):
    W, H = 0, 0
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    padding = 0.1
    W, H = int(W * (1 + padding)), int(H * (1 + padding))

    # Create a new SVG drawing
    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(W, H))
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            path_data = ['M {} {}'.format(XY[0, 0], XY[0, 1])]
            path_data += ['L {} {}'.format(x, y) for x, y in XY[1:]]
            dwg.add(dwg.path(d=' '.join(path_data), fill='none', stroke='black'))

    dwg.save()

    # Convert SVG to PNG
    try:
        cairosvg.svg2png(url=svg_path, write_to=svg_path.replace('.svg', '.png'))
    except Exception as e:
        print(f"Error during SVG to PNG conversion: {e}")


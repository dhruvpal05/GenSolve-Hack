# import matplotlib.pyplot as plt

# def plot(paths_XYs):
#     fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
#     for i, XYs in enumerate(paths_XYs):
#         c = 'C{}'.format(i % 10)
#         for XY in XYs:
#             ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
#     plt.show()
import numpy as np
import matplotlib.pyplot as plt

def plot(paths_XYs, colours=None):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    if colours is None:
        colours = ['b'] * len(paths_XYs)  # Default to blue if no colours are provided
    
    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.show()

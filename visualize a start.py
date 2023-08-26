# Import necessary libraries
from psychopy import visual, event, core
import numpy as np

# Create a window
win = visual.Window(size=(800, 600), units='pix')

# Define colors
yellow = (1, 1, 0)  # Yellow in RGB

# Create a Chinese flag-like star using ShapeStim with custom vertices
large_star_radius = 150
small_star_radius = 50
angle_offset = np.pi / 10  # Offset angle to start drawing the star

large_star_vertices = []
small_star_vertices = []

for i in range(5):
    angle = angle_offset + i * (2 * np.pi / 5)
    x_large = large_star_radius * np.cos(angle)
    y_large = large_star_radius * np.sin(angle)
    large_star_vertices.append((x_large, y_large))

    # Add small stars around the large star
    small_star_angle = angle + np.pi / 5
    for j in range(4):
        small_angle = small_star_angle + j * (2 * np.pi / 5)
        x_small = small_star_radius * np.cos(small_angle) + x_large
        y_small = small_star_radius * np.sin(small_angle) + y_large
        small_star_vertices.append((x_small, y_small))

# Create ShapeStim objects for the large and small stars
large_star = visual.ShapeStim(win, vertices=large_star_vertices, fillColor=yellow, lineColor=None)
small_stars = visual.ShapeStim(win, vertices=small_star_vertices, fillColor=yellow, lineColor=None)

# Draw the Chinese flag-like stars
# large_star.draw()
small_stars.draw()

# Update the window
win.flip()

# Wait for a response
event.waitKeys()

# Close the window
win.close()

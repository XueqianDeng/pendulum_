from psychopy import visual, event
import numpy as np

# Create a window
win = visual.Window(size=(800, 600), units='pix', fullscr=False)

# Create points for a half-circle curve
num_points = 50
angle_values = np.linspace(0, np.pi / 4, num_points)  # Angles from 0 to pi
x_values = np.cos(angle_values) * 100  # x = r * cos(angle)
y_values = np.sin(angle_values) * 100  # y = r * sin(angle)

# Create a polygon stimulus to connect the points
half_circle_curve = visual.ShapeStim(win, vertices=zip(x_values, y_values), fillColor=None, lineColor='blue')

# Draw the half-circle curve
half_circle_curve.draw()
win.flip()

# Wait for a key press to close the window
event.waitKeys()

# Close the window
win.close()

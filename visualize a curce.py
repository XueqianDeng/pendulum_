from psychopy import visual, event
import numpy as np

# Create a window
win = visual.Window(size=(800, 600), units='pix', fullscr=False)

# Create points for a quarter-circle curve
num_points = 50
angle_values = np.linspace(0, np.pi / 2, num_points)  # Angles from 0 to pi/2
x_values = np.cos(angle_values) * 100  # x = r * cos(angle)
y_values = np.sin(angle_values) * 100  # y = r * sin(angle)

# Combine points to create the quarter-circle curve
curve_points = list(zip(x_values, y_values))

# Create a line stimulus to represent the quarter-circle curve
quarter_circle_curve = visual.Line(win, start=curve_points[0], end=curve_points[-1], lineColor='red')

# Draw the quarter-circle curve
quarter_circle_curve.draw()
win.flip()

# Wait for a key press to close the window
event.waitKeys()

# Close the window
win.close()

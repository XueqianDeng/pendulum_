from psychopy import visual, event
import numpy as np

# Create a window
win = visual.Window(size=(800, 600), units='pix', fullscr=False)
radius = 100
# Create points for a quarter-circle curve
num_points = 50
angle_values = np.linspace(0, np.pi, num_points)  # Angles from 0 to pi/2
x_values_out = np.cos(angle_values) * radius  # x = r * cos(angle)
y_values_out = np.sin(angle_values) * radius  # y = r * sin(angle)
x_values_in = np.cos(angle_values) * (radius - 20)
y_values_in = np.cos(angle_values) * (radius - 20)
x_values = (x_values_out, x_values_in)
y_values = [y_values_out, y_values_in]
# Create a polygon stimulus to represent the quarter-circle curve
curve = visual.ShapeStim(win, vertices=list(zip(x_values, y_values)), fillColor=None, lineColor='red')

# Draw the quarter-circle curve
curve.draw()
win.flip()

# Wait for a key press to close the window
event.waitKeys()

# Close the window
win.close()

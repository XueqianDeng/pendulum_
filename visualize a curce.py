from psychopy import visual, event
import numpy as np

# Create a window
win = visual.Window(size=(800, 600), units='pix', fullscr=False)

# Create points along a curve
num_points = 100
x_values = np.linspace(-200, 200, num_points)
y_values = np.sin(x_values / 100) * 100  # Example curve equation

# Create a polygon stimulus to connect the points
curve = visual.ShapeStim(win, vertices=list(zip(x_values, y_values)), fillColor=None, lineColor='green')

# Draw the curve
curve.draw()
win.flip()

# Wait for a key press to close the window
event.waitKeys()

# Close the window
win.close()

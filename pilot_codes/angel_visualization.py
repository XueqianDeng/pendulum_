import numpy as np
import matplotlib.pyplot as plt

angle_degrees = 330
angle_radians = np.radians(angle_degrees)

# Create the figure and axes
fig, ax = plt.subplots()

# Plot the line segment
ax.plot([0, -np.cos(angle_radians)], [0, np.sin(angle_radians)], 'r')

# Set the aspect ratio of the plot to be equal
ax.set_aspect('equal')

# Set the limits of the plot
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])

# Set labels and title
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Visualization of a 30-degree angle')

# Display the plot
plt.show()
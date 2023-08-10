import numpy as np
from psychopy import visual, core, event

# Set up window
win = visual.Window(size=(800, 600), fullscr=False, allowGUI=False)

# Define parameters
pendulum_length = 200  # Length of the pendulum arm
pendulum_mass = 10  # Mass of the pendulum bob
pendulum_angle = np.pi / 4  # Initial angle of the pendulum
g = 9.8  # Acceleration due to gravity

# Create pendulum components
ground = visual.Line(win, start=(-400, -300), end=(400, -300), lineColor='black', lineWidth=2)
pivot = visual.Circle(win, radius=10, pos=(0, -300), fillColor='black')
pendulum_arm = visual.Rect(win, width=10, height=pendulum_length, pos=(0, -300 + pendulum_length / 2), fillColor='blue')
bob = visual.Circle(win, radius=20, pos=(0, -300+pendulum_length), fillColor='red')

# Set initial pendulum position
pendulum_arm.setOri(pendulum_angle)

# Start animation loop
clock = core.Clock()
while True:
    # Update pendulum angle based on physics
    angle_acceleration = -g / pendulum_length * np.sin(pendulum_arm.getOri())
    pendulum_angle += angle_acceleration * clock.getTime()

    # Update pendulum components
    pendulum_arm.setOri(pendulum_angle)
    bob.setPos((pendulum_length * np.sin(pendulum_angle), -300 + pendulum_length * np.cos(pendulum_angle)))

    # Draw components
    ground.draw()
    pivot.draw()
    pendulum_arm.draw()
    bob.draw()
    win.flip()

    # Check for quit event
    if 'escape' in event.getKeys():
        break

    # Reset clock
    clock.reset()

# Clean up
win.close()
core.quit()

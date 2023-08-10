"""
Inverted Pendulum Animation with Physics and Air Friction
Author: OpenAI (modified by [Your Name])

This script animates an inverted pendulum using PsychoPy.
The pendulum is represented by a line segment, and a big ball is placed at the top of the pendulum tip.
The animation loop continuously updates the pendulum angle and displays the pendulum swinging.
Press the 'escape' key to exit the animation.

Dependencies:
- NumPy
- PsychoPy
"""

import numpy as np
from psychopy import visual, event, core

# Pendulum Parameters
pendulum_length = 200
pendulum_mass = 1.0
pendulum_angle = np.pi / 4  # Initial angle (45 degrees)
pendulum_angular_velocity = 0.0
gravity = 9.8
drag_coefficient = 0.1  # Adjust the drag coefficient as needed

# Window Parameters
window_size = [800, 600]
window = visual.Window(window_size, units='pix', fullscr=False)

# Pendulum Visuals
pivot = visual.Rect(window, width=10, height=10, fillColor='black')
pendulum = visual.Line(window, start=(0, 0), end=(pendulum_length * np.sin(pendulum_angle),
                                                   -pendulum_length * np.cos(pendulum_angle)),
                       lineColor='black', lineWidth=2)
ball_radius = 20
ball = visual.Circle(window, radius=ball_radius, fillColor='red', lineColor='black', lineWidth=2)

# Animation Loop
while True:
    # Update Pendulum State
    pendulum_angular_acceleration = (-gravity / pendulum_length * np.sin(pendulum_angle)) - (
            drag_coefficient * pendulum_angular_velocity)
    pendulum_angular_velocity += pendulum_angular_acceleration
    pendulum_angle += pendulum_angular_velocity

    # Update Pendulum Visuals
    pendulum.start = (0, 0)
    pendulum.end = (pendulum_length * np.sin(pendulum_angle), -pendulum_length * np.cos(pendulum_angle))
    ball_pos = (pendulum_length * np.sin(pendulum_angle), -pendulum_length * np.cos(pendulum_angle))

    # Draw Pendulum and Ball
    pivot.draw()
    pendulum.draw()
    ball.pos = ball_pos
    ball.draw()
    window.flip()

    # Check for Exit
    if event.getKeys(keyList=['escape']):
        break

# Cleanup
window.close()
core.quit()

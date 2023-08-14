from psychopy import visual, event, core

# Set up the window
win = visual.Window(size=(800, 600), fullscr=False)

# Pendulum properties
pendulum_length = 200
pendulum_angle = 0  # Starting angle (in degrees)
pendulum_angular_velocity = 0.2  # Angular velocity of the pendulum

# Pendulum visual components
pendulum_center = visual.Circle(win, radius=10, pos=(0, 0), fillColor='black')
pendulum_rod = visual.Line(win, start=(0, 0), end=(0, -pendulum_length), lineWidth=2)
pendulum_ball = visual.Circle(win, radius=20, fillColor='blue', lineColor='black')

# Simulation loop
while True:
    # Check for key press to quit
    if 'escape' in event.getKeys():
        break

    # Update pendulum angle
    pendulum_angle += pendulum_angular_velocity

    # Limit the pendulum angle to prevent it from falling onto the ground
    if pendulum_angle >= 90:
        pendulum_angle = 90
        pendulum_angular_velocity = 0  # Stop the pendulum from moving

        # Pendulum has fallen, simulate breaking
        pendulum_ball.fillColor = 'red'
        pendulum_rod.lineColor = 'red'

    # Update pendulum visuals
    pendulum_rod.end = (pendulum_length * pendulum_angle / 90, -pendulum_length)
    pendulum_ball.pos = pendulum_rod.end

    # Clear the window
    win.flip()

    # Draw pendulum components
    pendulum_center.draw()
    pendulum_rod.draw()
    pendulum_ball.draw()

    # Update the window
    win.flip()

# Close the window
win.close()

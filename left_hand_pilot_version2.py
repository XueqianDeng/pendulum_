import psychopy
from psychopy import visual, core, event, monitors
from psychopy.hardware import keyboard
from psychopy.visual import circle
import pandas as pd
import numpy as np
import nidaqmx as ni
from nidaqmx.constants import WAIT_INFINITELY
import json
import websocket
import time
import os
import asyncio
import random
import math
import pickle
import scipy as signal

# Text Equipment with NI MAX

# force_keyboard table:

# Dev2/ai0 positive sign, left hand thumb
# Dev2/ai0 negative sign, left hand index finger
# Dev2/ai1 positive sign, left hand middle finger
# Dev2/ai1 negative sign, left hand ring finger
# Dev2/ai2 positive sign, left hand pinky
# Dev2/ai2 negative sign, right hand thumb
# Dev2/ai3 positive sign, right hand index finger
# Dev2/ai3 negative sign, right hand middle finger
# Dev2/ai4 positive sign, right hand ring finger
# Dev2/ai4 negative sign, right hand pinky

# Subject set up


global running, current_data, trials_run, trial_count, ofile, maintaining, already_in_range, init_time
global pendulum_length, pendulum_mass, pendulum_angle, pendulum_angular_velocity, gravity, drag_coefficient
global muscle_left, muscle_right, muscle_amplification, inertia, stiffness, pendulum_length_visual_coff
global conversion_unit_for_one_newton, dt, output_csv_array, time_taken, results

subject_label = "Hokin_Second_Time_" + "Right_Hand"
Gravity_Level = 40  # [10 15 20 25 30 35 40]
trials_run = 30
results = 0

# Directory Making
general_directory = "data/" + subject_label

# Check if the directory already exists before creating it
if not os.path.exists(general_directory):
    # Create the directory
    os.mkdir(general_directory)
    print(f"Directory '{subject_label}' created successfully.")
else:
    print(f"Directory '{subject_label}' already exists.")

general_directory = "data/" + subject_label + "/" + "Gravity" + str(Gravity_Level) + "/"
# Check if the directory already exists before creating it
if not os.path.exists(general_directory):
    os.mkdir(general_directory)
    print(f"Directory '{subject_label}' created successfully.")
else:
    print(f"Directory '{subject_label}' already exists.")

# Global Variables
input_mapping = ['Dev2/ai0', 'Dev2/ai1']
# left [thumb and index finger] and [middle and ring finger]

nsamples = 10
samplerate = 1000
center = (0, 50)


def reset():
    global running, current_data, trials_run, trial_count, ofile, maintaining, already_in_range, init_time
    global pendulum_length, pendulum_mass, pendulum_angle, pendulum_angular_velocity, gravity, drag_coefficient
    global muscle_left, muscle_right, muscle_amplification, inertia, stiffness, pendulum_length_visual_coff
    global conversion_unit_for_one_newton, dt
    conversion_unit_for_one_newton = 0.059  # Conversion 0.059 in forcekeyboard is 1 Newton
    pendulum_length = 50  # in meters
    pendulum_length_visual_coff = 4  # for visualization conversion, should be 200 in multiplication
    pendulum_mass = 1  # 1 kilogram
    pendulum_angle = np.pi / 4  # Initial angle (45 degrees)
    pendulum_angular_velocity = 0.0
    gravity = Gravity_Level  # meter / second square
    stiffness = 3
    inertia = pendulum_mass * pendulum_length * pendulum_length
    drag_coefficient = 5000  # Adjust the drag coefficient as needed
    dt = 0.05  # in second
    muscle_amplification = 100
    muscle_left = 0
    muscle_right = 0


def flow_maintainence(pend_angle):
    while pend_angle > 2 * np.pi:
        pend_angle = pend_angle - 2 * np.pi
    while pend_angle < 0:
        pend_angle = pend_angle + 2 * np.pi
    return pend_angle


def experiment_synchronize():
    global running, current_data, trials_run, trial_count, ofile, maintaining, already_in_range, init_time
    global pendulum_length, pendulum_mass, pendulum_angle, pendulum_angular_velocity, gravity, drag_coefficient
    global muscle_left, muscle_right, muscle_amplification, inertia, stiffness, pendulum_length_visual_coff
    global conversion_unit_for_one_newton, dt, output_csv_array, time_taken, results
    last_time = time.time()
    while running:
        keys = event.getKeys(keyList=['escape'])
        if keys:
            window.close()
            core.quit()
            print("Ggg")
        if np.sum(np.sum(current_data)) != 0:
            muscle_left = np.mean(current_data[:, 0])
            muscle_right = np.mean(current_data[:, -1])

        # Muscle Force Conversion
        muscle_right = np.abs(muscle_right) / conversion_unit_for_one_newton * muscle_amplification
        muscle_left = - np.abs(muscle_left) / conversion_unit_for_one_newton * muscle_amplification

        # Time Elapsed
        current_time = time.time()
        elapsed_time = current_time - last_time
        last_time = current_time
        print("Time", elapsed_time)

        # Pendulum Physics
        pendulum_angular_acceleration = pendulum_mass * gravity * pendulum_length * np.sin(pendulum_angle) \
                                        - drag_coefficient * pendulum_angular_velocity - stiffness * \
                                        (np.abs(muscle_left) + np.abs(muscle_right)) * pendulum_angle + (
                                                    muscle_left + muscle_right)
        pendulum_angular_acceleration = pendulum_angular_acceleration / inertia * dt
        print("acc", pendulum_angular_acceleration)
        pendulum_angular_velocity += pendulum_angular_acceleration
        print("velo", pendulum_angular_velocity)
        pendulum_angle += pendulum_angular_velocity

        # Record Data
        with ni.Task() as read_task:
            for i in input_mapping:
                read_task.ai_channels.add_ai_voltage_chan(i)
            read_task.timing.cfg_samp_clk_timing(rate=samplerate, source='OnboardClock',
                                                 samps_per_chan=nsamples)
            indata = read_task.read(nsamples, timeout=WAIT_INFINITELY)
            current_data = np.asarray(indata).T
        record_data = np.append(np.mean(current_data, axis=0), current_time)
        ofile.write(str(record_data) + "\n")
        output_csv_array = np.vstack((output_csv_array, record_data))

        # Update Pendulum Visuals
        pendulum.start = center
        pendulum_end_x = center[0] + pendulum_length * pendulum_length_visual_coff * np.sin(pendulum_angle)
        pendulum_end_y = center[1] + pendulum_length * pendulum_length_visual_coff * np.cos(pendulum_angle)
        pendulum.end = (pendulum_end_x, pendulum_end_y)
        ball_pos = (pendulum_end_x, pendulum_end_y)

        # Draw Pendulum and Ball
        pivot.draw()
        pendulum.draw()
        ball.pos = ball_pos
        ball.draw()
        ground.draw()
        window.flip()

        # Reset angle if greater overflow or underflow
        if 90 < np.degrees(pendulum_angle) or -90 > np.degrees(pendulum_angle):
            maintaining = True
            message = visual.TextStim(window, text="You Fail", height=30, color='black', pos=[0, 100])
            message.draw()
            window.flip()
            core.wait(0.5)

        #  Maintaining Check Code
        print("Here,", np.degrees(pendulum_angle))
        #  if -10 < np.degrees(pendulum_angle) < 10 and not already_in_range:
        #    already_in_range = True
        #     init_time = time.time()
        # if not (-10 < np.degrees(pendulum_angle) < 10) and already_in_range:
        #     already_in_range = False
        #     init_time = 0
        # if -10 < np.degrees(pendulum_angle) < 10 and already_in_range:
        #     timer = time.time()
        #     if 15 > timer - init_time > 3:
        #         message = visual.TextStim(window, text="You Succeed", height=30, color='black', pos=[0, 100])
        #         core.wait(0.5)
        #         # Draw the text stimulus
        #         message.draw()
        #         window.flip()
        #         maintaining = True
        time_taken = time.time() - current_time

        if time_taken > 6:
            message = visual.TextStim(window, text="You Succeed", height=30, color='black', pos=[0, 100])
            core.wait(0.5)
            # Draw the text stimulus
            message.draw()
            window.flip()
            maintaining = True
            results = 1

        if maintaining:
            trial_count += 1
            reset()
            ofile.close()
            df = pd.DataFrame(data=output_csv_array[1:], columns=['u_1', 'u_2', 'angle', 'velocity', 'acceleration',
                                                                  'results', 'time'])
            df.to_csv(general_directory + str(trial_count) + ".csv", index=False)
            ofile = open(general_directory + str(trial_count) + ".txt", "w")
            ofile.write(subject_label + "\n")
            ofile.write(" ".join(input_mapping) + "\n")
            output_csv_array = np.array([0, 0, 0, 0, 0, 0, 0])
            # Create a text stimulus
            message = visual.TextStim(window, text="Wait for the next game", height=30, color='black', pos=[0, 100])
            # Draw the text stimulus
            message.draw()
            window.flip()
            # Wait for 3 seconds
            core.wait(1)
            pendulum_angle = np.pi / 4  # Initial angle (45 degrees)
            pendulum_angle = random.uniform(np.pi / 6 - np.pi / 2, np.pi / 3 - np.pi / 2) + random.randint(0, 1) * np.pi / 2
            # randomly initialize between [-60 -30] and randomly add 90 to get the positive range
            maintaining = False
            results = 0

        if trial_count > trials_run:
            running = False


## Main Code


# Data Parameters
reset()
N_channels = 2  # recording channels
current_data = np.zeros([N_channels, nsamples])

# Window Parameters
window_size = [1900, 1200]
window_position = [0, 25]
window = visual.Window(window_size, units='pix', fullscr=False, pos=window_position)

# Pendulum Visuals
pivot = visual.Rect(window, width=10, height=10, fillColor='black')
pivot.setPos(center)
pendulum = visual.Line(window, start=center, end=center,
                       lineColor='black', lineWidth=2)
ball_radius = 20
ball = visual.Circle(window, radius=ball_radius, fillColor='red', lineColor='black', lineWidth=2)
ground = visual.Line(window, start=(-100, center[1]), end=(100, center[1]), lineColor='black', lineWidth=2)

message = visual.TextStim(window, text="Try to balance the inverted pendulum", height=30, color='black', pos=[0, 100])
message.draw()
window.flip()
# Wait for 3 seconds
core.wait(3)

# Setting up
trial_count = 0
running = True
maintaining = False
# already_in_range = False
ofile = open(general_directory + str(trial_count) + ".txt", "w")
ofile.write(subject_label + "\n")
ofile.write(" ".join(input_mapping) + "\n")
output_csv_array = np.array([0, 0, 0, 0, 0, 0, 0])

init_time = time.time()

experiment_synchronize()

window.close()
core.quit()

import psychopy
from psychopy import visual, core, event, monitors
from psychopy.hardware import keyboard
from psychopy.visual import circle
import numpy as np
import pandas as pd
import numpy as np
import nidaqmx as ni
from nidaqmx.constants import WAIT_INFINITELY
import json
import websocket
import time
import asyncio
import random
import math
import pickle
import scipy as signal

# Global Variables
input_mapping = ['Dev2/ai0', 'Dev2/ai1']
nsamples = 10
samplerate = 1000


def play_rec(data, samplerate, input_mapping, output_mapping):
    """Simultaneous playback and recording though NI device.
    Parameters:
    -----------
    data: array_like, shape (nsamples, len(output_mapping))
      Data to be send to output channels.
    samplerate: int
      Samplerate
    input_mapping: list of str
      Input device channels
    output_mapping: list of str
      Output device channels
    Returns
    -------
    ndarray, shape (nsamples, len(input_mapping))
      Recorded data
    """
    devices = ni.system.System.local().devices
    data = np.asarray(data).T
    nsamples = data.shape[1]

    with ni.Task() as read_task, ni.Task() as write_task:
        for i, o in enumerate(output_mapping):
            aochan = write_task.ao_channels.add_ao_voltage_chan(
                o,
                min_val=devices[o].ao_voltage_rngs[0],
                max_val=devices[o].ao_voltage_rngs[1]
            )
            min_data, max_data = np.min(data[i]), np.max(data[i])
            if ((max_data > aochan.ao_max) | (min_data < aochan.ao_min)).any():
                raise ValueError(
                    f"Data range ({min_data:.2f}, {max_data:.2f}) exceeds output range of "
                    f"{o} ({aochan.ao_min:.2f}, {aochan.ao_max:.2f}).")
        for i in input_mapping:
            read_task.ai_channels.add_ai_voltage_chan(i)

        for task in (read_task, write_task):
            task.timing.cfg_samp_clk_timing(rate=samplerate, source='OnboardClock',
                                            samps_per_chan=nsamples)

        # trigger write_task as soon as read_task starts
        write_task.triggers.start_trigger.cfg_dig_edge_start_trig(
            read_task.triggers.start_trigger.term)
        # squeeze as Task.write expects 1d array for 1 channel
        write_task.write(data.squeeze(), auto_start=False)
        # write_task doesn't start at read_task's start_trigger without this
        write_task.start()
        # do not time out for long inputs
        indata = read_task.read(nsamples, timeout=WAIT_INFINITELY)
    return np.asarray(indata).T


def query_devices():
    local = ni.system.System.local()
    for device in local.devices:
        print(f'Device Name: {device.name}, Product Type: {device.product_type}')
        print('Input channels:', [chan.name for chan in device.ai_physical_chans])
        print('Output channels:', [chan.name for chan in device.ao_physical_chans])


# Function to listen to force keyboard and update the data
async def listen():
    """Simultaneous playback and recording though NI device.
    Parameters:
    -----------
    data: array_like, shape (nsamples, len(output_mapping))
      Data to be send to output channels.
    samplerate: int
      Samplerate
    input_mapping: list of str
      Input device channels
    output_mapping: list of str
      Output device channels
    Returns
    -------
    ndarray, shape (nsamples, len(input_mapping))
      Recorded data
    """
    global running, current_data
    while running:
        with ni.Task() as read_task:
            for i in input_mapping:
                read_task.ai_channels.add_ai_voltage_chan(i)
            read_task.timing.cfg_samp_clk_timing(rate=samplerate, source='OnboardClock',
                                                samps_per_chan=nsamples)
            indata = read_task.read(nsamples, timeout=WAIT_INFINITELY)
            current_data = np.asarray(indata).T
            print(current_data)


async def experiment():
    global running, current_data, trials_run, trial_count
    global pendulum_length, pendulum_mass, pendulum_angle, pendulum_angular_velocity, gravity, drag_coefficient
    global muscle_left, muscle_right
    print("Reach Here")
    while running:
        keys = event.getKeys(keyList=['escape'])
        if keys:
            window.close()
            core.quit()
        if np.sum(np.sum(current_data)) != 0:
            last_row = current_data[-1]
            muscle_left = last_row[0]
            muscle_right = last_row[-1]

        # Pendulum Physics
        pendulum_angular_acceleration = (-gravity / pendulum_length * np.sin(pendulum_angle)) - (
                drag_coefficient * pendulum_angular_velocity)
        pendulum_angular_velocity += pendulum_angular_acceleration
        pendulum_angle += pendulum_angular_velocity + muscle_left - muscle_right
        current_time = time.time()

        # Record Data
        record_data = np.append(current_data[-1], current_time)
        ofile.write(record_data + "\n")

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

        if pendulum_angle == 180:
            ofile = open("data/" + subject_label + str(trial_count) + ".txt", "w")
            ofile.write(subject_label + "\n")
            ofile.write(" ".join(input_mapping) + "\n")
            trial_count += 1
            # Create a text stimulus
            message = visual.TextStim(window, text="Wait for the next game", height=30, color='black')
            # Draw the text stimulus
            message.draw()
            window.flip()
            # Wait for 3 seconds
            core.wait(3)

        if trial_count > trials_run:
            running = False


async def main():
    await asyncio.gather(listen(), experiment())


def experiment_synchronize():
    global running, current_data, trials_run, trial_count, ofile
    global pendulum_length, pendulum_mass, pendulum_angle, pendulum_angular_velocity, gravity, drag_coefficient
    global muscle_left, muscle_right

    while running:

        keys = event.getKeys(keyList=['escape'])
        if keys:
            window.close()
            core.quit()
        if np.sum(np.sum(current_data)) != 0:
            muscle_left = np.mean(current_data[:, 0])
            muscle_right = np.mean(current_data[:, -1])

        # Pendulum Physics
        pendulum_angular_acceleration = (-gravity / pendulum_length * np.sin(pendulum_angle)) - (
                drag_coefficient * pendulum_angular_velocity)
        pendulum_angular_velocity += pendulum_angular_acceleration
        pendulum_angle += pendulum_angular_velocity + muscle_left + muscle_right

        # Record Data
        current_time = time.time()
        with ni.Task() as read_task:
            for i in input_mapping:
                read_task.ai_channels.add_ai_voltage_chan(i)
            read_task.timing.cfg_samp_clk_timing(rate=samplerate, source='OnboardClock',
                                                 samps_per_chan=nsamples)
            indata = read_task.read(nsamples, timeout=WAIT_INFINITELY)
            current_data = np.asarray(indata).T
            print(current_data)
        record_data = np.append(np.mean(current_data), current_time)
        print(record_data)
        ofile.write(str(record_data) + "\n")

        # Update Pendulum Visuals
        pendulum.start = (0, 0)
        pendulum.end = (pendulum_length * np.sin(pendulum_angle), -pendulum_length * np.cos(pendulum_angle))
        ball_pos = (pendulum_length * np.sin(pendulum_angle), -pendulum_length * np.cos(pendulum_angle))

        print("Acc", pendulum_angular_acceleration)

        # Draw Pendulum and Ball
        pivot.draw()
        pendulum.draw()
        ball.pos = ball_pos
        ball.draw()
        window.flip()

        if pendulum_angle == 180:
            trial_count += 1
            ofile = open("data/" + subject_label + str(trial_count) + ".txt", "w")
            ofile.write(subject_label + "\n")
            ofile.write(" ".join(input_mapping) + "\n")
            # Create a text stimulus
            message = visual.TextStim(window, text="Wait for the next game", height=30, color='black')
            # Draw the text stimulus
            message.draw()
            window.flip()
            # Wait for 3 seconds
            core.wait(3)

        if trial_count > trials_run:
            running = False

## Main Code

#Test Devices
query_devices()
outdata = np.random.normal(size=(5000, 1)) * 0.01
indata = play_rec(outdata,
                 samplerate=1000,
                 input_mapping=['Dev2/ai0', 'Dev2/ai1', 'Dev2/ai2'],
                 output_mapping=['Dev2/ao0'])
print(indata)

# Data Parameters
subject_label = "Test"
N_channels = 2 # recording channels
N_points = 20000 # pre_occupy data points
current_data = np.zeros([N_channels, N_points])

# Pendulum Parameters
pendulum_length = 200
pendulum_mass = 1.0
pendulum_angle = np.pi / 4  # Initial angle (45 degrees)
pendulum_angular_velocity = 0.0
gravity = 9.8
drag_coefficient = 0.1  # Adjust the drag coefficient as needed
muscle_left = 0
muscle_right = 0

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

# Setting up
trials_run = 100
trial_count = 0
running = True
ofile = open("data/" + subject_label + str(trial_count) + ".txt", "w")
ofile.write(subject_label + "\n")
ofile.write(" ".join(input_mapping) + "\n")

# asyncio.get_event_loop().run_until_complete(main())
experiment_synchronize()

window.close()
core.quit()

import numpy as np
import psychopy
import matplotlib.pyplot as plt
from psychopy import visual, core, event
import random
import os
#establish in phase out phase (behavioral data, RT, accuracy)
#how big is the effect of the phase difference
#how big is the size of the character:Size: each character was of the same size and subtended 1.5° × 1.5° of visual angle
#visual angle: A rectangular cue (1.6° × 1.6°) appeared (approximately 5.5°) to either the left or the right of the fixation
#use grating first? grating detection? is it ok
#check eeg response first? what do i want to measure? synchrony?
#how to send trigger to EEG
#create another similar experiment with grating
##create another similar experiment with jitter stimuli
#SOA need to be have same probability
#The target character (or noncharacter) then was presented in the same location occupied by the cue or in the opposite location.
# Set the viewing distance in centimeters
viewing_distance = 60
# Create a window to display the experiment
win = visual.Window(size=[1470, 956], fullscr=False, color='grey', units='height',monitor='testMonitor')

frame_left = visual.Rect(win, width=10, height=10, units='deg',fillColor='white', lineColor='white', pos=(-5, 0))
frame_right = visual.Rect(win, width=10, height=10, units='deg',fillColor='white', lineColor='white', pos=(5, 0))
fixation = visual.TextStim(win, text="x", height=1, units='deg',color='white', pos=(0, 0))

# Define the parameters for the normal flash
flash_duration = 0.1
flash_interval = 0.2

# Loop for the flash train
total_trials = 6
total_flashes = 10

for trial_count in range(total_trials):
    # Generate time points for the sine wave
    total_duration = 5
    frequency = 5
    time_points = np.linspace(0, total_duration, num=1000)
    sine_wave = np.sin(2 * np.pi * frequency * time_points - np.pi/2 - np.pi)

    # Create a figure for plotting the sine wave
    fig, ax = plt.subplots()
    ax.plot(time_points, sine_wave)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_xlim([0, 3])

    for i in range(total_flashes):
        # Flash the frames by drawing and updating the window
        for frame in [frame_left, frame_right]:
            frame.draw()
            fixation.draw()
            duration = flash_duration
            interval = flash_interval

        # Mark the flash start time on the graph
        flash_start_time = (i + 1) * interval
        ax.axvline(flash_start_time, color='blue', linestyle='--')

        # Display the plot
        plt.pause(0.001)

        # Clear the frames by drawing a blank window and updating the window
        win.flip()
        core.wait(duration)

        # Mark the flash end time on the graph
        flash_end_time = flash_start_time + flash_duration
        ax.axvline(flash_end_time, color='red', linestyle='--')

        # Display the plot
        plt.pause(0.001)

        # Clear the frames by drawing a blank window and updating the window
        win.flip()

    # Choose the SOA pseudo-randomly (100, 300 is in phase, 150, 350 is out of phase)
    in_phase = [100, 300]
    out_phase = [150, 350]

    if random.random() < 0.5:
         soa = random.choice(in_phase)
    else:
         soa = random.choice(out_phase)

    x = [5.5, -5.5]
    position = random.choice(x)
    print(soa)

    # Present the visual cue with the chosen SOA
    cue_duration = 0.05
    core.wait(soa / 1000)  # Convert SOA from ms to seconds
    visual_cue = visual.Rect(win, width=1.5, height=1.5, units='deg',fillColor='black', lineColor='black', lineWidth=10, pos=(position, 5))
    visual_cue.draw()
    fixation.draw()
    win.flip()
    core.wait(cue_duration)
    fixation.draw()
    win.flip()
    fixation.draw()

    # Interstimulus interval
    core.wait(0.15)
    # Display a random word
    folder_path = '/Users/sc/Desktop/Psychopy/G1-3'
    # Get a list of all JPEG files in the folder
    jpeg_files = [file for file in os.listdir(folder_path) if file.endswith(".jpg")]
    random_files = random.sample(jpeg_files, 1)
    random_file = random_files[0]
    jpeg_files.remove(random_file)  # Remove the selected file from the list

    file_path = os.path.join(folder_path, random_file)
    word_image = visual.ImageStim(win, image=file_path, size=1.5,units='deg', pos=(position, 0))
    fixation.draw()
    word_image.draw()
    fixation.draw()
    win.flip()
    core.wait(0.15)  # Display for 150ms (same as Luo 2015)
    win.flip()

    # Mark the cue time on the graph
    cue_start_time = 2.1 + (soa / 1000)
    ax.axvline(cue_start_time, color='orange', linestyle='--', label='cue')
    # Display the plot
    plt.pause(0.001)
    win.flip()
    cue_end_time = cue_start_time + cue_duration
    ax.axvline(cue_end_time, color='green', linestyle='--', label='cue end')
    # Display the plot
    plt.pause(0.001)
    win.flip()
    word_start_time = cue_end_time + 0.15
    ax.axvline(word_start_time, color='purple', linestyle='--', label='word')

    # Display the plot
    plt.pause(0.001)

    # Key response
    keys = event.waitKeys(keyList=['1', '0'])
    win.flip()
    response = keys[0]
    print(response)

    # Update the plot legend for the current trial
    ax.legend()

    # Close the figure for the current trial
    plt.close(fig)

# Show the plot with all the trials' data
plt.show()


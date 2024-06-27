import numpy as np
import matplotlib.pyplot as plt
import random
import os
import time

# Enable interactive mode for Matplotlib
plt.ion()

# Generate time points for the sine wave
total_duration = 2
frequency = 5
time_points = np.linspace(0, total_duration, num=1000)
sine_wave = np.sin(2 * np.pi * frequency * time_points)

# Create a figure for plotting the sine wave
fig, ax = plt.subplots()
ax.plot(time_points, sine_wave)
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_xlim([0, total_duration])

# Display the plot
plt.show()

# Outer loop for trials
total_trials = 10
total_flashes = 10
flash_duration = 0.1
flash_interval = 0.1

# Create the white frames
frame_left = plt.Rectangle((-150, 0), 300, 300, fill=True, color='white')
frame_right = plt.Rectangle((150, 0), 300, 300, fill=True, color='white')

# Create a window to display the experiment
plt.figure()
ax.add_patch(frame_left)
ax.add_patch(frame_right)
plt.draw()

# Loop for trials
for trial_count in range(total_trials):
    # Generate new random intervals and durations for each trial in the 'jitter' condition
    intervals = [random.uniform(0.1, 0.2), random.uniform(0.2, 0.5), random.uniform(0.01, 0.1),
                 random.uniform(0.02, 0.2)]
    while len(intervals) < total_flashes:
        intervals.append(random.uniform(0.01, 0.5))
    durations = [(total_duration - sum(intervals)) / total_flashes] * (total_flashes - 1)
    durations.append(total_duration - sum(durations))

    # Loop for the flash train
    for i in range(total_flashes):
        # Randomly choose between normal flash and jitter flash
        if random.random() < 0.5:
            condition = 'normal'
            frame_to_flash = [frame_left, frame_right]
            duration = flash_duration
            interval = flash_interval
        else:
            condition = 'jitter'
            frame_to_flash = [frame_left, frame_right]
            duration = durations[i]
            interval = intervals[i]

        # Flash the frames by drawing and updating the plot
        fig.canvas.draw()
        plt.pause(interval)
        fig.canvas.draw()
        plt.pause(duration)

    # Choose the SOA pseudo-randomly
    soa_options = [100, 200, 300, 400]
    soa = random.choice(soa_options)
    x = [150, -150]
    position = random.choice(x)

    # Present the visual cue with the chosen SOA
    cue_duration = 0.05
    time.sleep(soa / 1000)  # Convert SOA from ms to seconds
    visual_cue = plt.Rectangle((position, 50), 10, 10, fill=True, color='black')
    ax.add_patch(visual_cue)
    plt.draw()

    # Update the plot
    ax.axvline(x=trial_count * total_duration, color='orange', linestyle='--', label='Stimulus Onset')
    ax.axvline(x=trial_count * total_duration + np.random.uniform(0, total_duration), color='g', linestyle='--',
               label='Interval')
    ax.axvline(x=trial_count * total_duration + (soa / 1000) + 0.15, color='blue', linestyle='--',
               label='Word Stimulus')
# Update the plot
plt.pause(0.001)
plt.draw()

# Interstimulus interval
time.sleep(0.15)

# Display a random word
folder_path = '/Users/sc/Desktop/Psychopy/G1-3'
# Get a list of all JPEG files in the folder
jpeg_files = [file for file in os.listdir(folder_path) if file.endswith(".jpg")]
random_file = random.choice(jpeg_files)
jpeg_files.remove(random_file)  # Remove the selected file from the list

file_path = os.path.join(folder_path, random_file)
word_image = plt.imread(file_path)
plt.figure()
plt.imshow(word_image)
plt.show(block=False)
plt.pause(0.05)  # Display for 100ms
plt.close()

# Key response
response = None
while response not in ['1', '0', 'esc']:
    response = input("Press '1' or '0' and press Enter (or 'esc' to end):")
    if response == 'esc':
        break
    else:
        print(response)


plt.close(fig)

from psychopy import visual, core, event
import random

# Create a window to display the experiment
win = visual.Window(size=[1470, 956], fullscr=True,color='grey', units='pix')

# Create the white frames
frame_left = visual.Rect(win, width=200, height=200, fillColor='white', lineColor='white', lineWidth=2000, pos=(-150, 0))
frame_right = visual.Rect(win, width=200, height=200, fillColor='white', lineColor='white', lineWidth=100, pos=(150, 0))

# Define the parameters for the flash train
total_trials = 10
total_flashes = 10

# Define the parameters for the normal flash
flash_duration = 0.1
flash_interval = 0.1

# Define the parameters for the jitter flash
total_duration = 2
intervals = [random.uniform(0.1, 0.2), random.uniform(0.2, 0.5), random.uniform(0.01, 0.1), random.uniform(0.02, 0.2)]
while len(intervals) < total_flashes:
    intervals.append(random.uniform(0.01, 0.5))
durations = [(total_duration - sum(intervals)) / total_flashes] * (total_flashes - 1)
durations.append(total_duration - sum(durations))

# Check if the total duration of jitter flashes exceeds the specified time
total_duration_check = sum(durations)
print(sum(durations))
if total_duration_check > total_duration:
    print("Total duration of jitter flashes exceeds the specified time.")

# Outer loop for trials
trial_count = 0
while trial_count < total_trials:
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

        # Flash the frames by drawing and updating the window
        for frame in frame_to_flash:
            frame.draw()
        win.flip()

        #core.wait(flash_interval)
        win.flip()

        # Clear the frames by drawing a blank window and updating the window
        core.wait(interval)
    print(condition)
    print(duration)
    print(interval)
    
    # Choose the SOA pseudo-randomly
    soa_options = [100, 110]
    soa = random.choice(soa_options)
    x=[150,-150]
    position = random.choice(x)
    print(soa)
    
    # Present the visual cue with the chosen SOA
    cue_duration = 0.1
    core.wait(soa / 1000)  # Convert SOA from ms to seconds
    visual_cue = visual.Rect(win, width=50, height=50, fillColor='black', lineColor='black', lineWidth=50, pos=(position, 0))
    visual_cue.draw()
    win.flip()
    core.wait(cue_duration)

    trial_count += 1

# Close the window
win.close()
core.quit()
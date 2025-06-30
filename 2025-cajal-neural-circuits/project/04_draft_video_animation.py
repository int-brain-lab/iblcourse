
# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define time window for the animation
frame_rate = 25
start_frame = 15090
end_frame = 15300
start_time = start_frame / frame_rate
end_time = end_frame / frame_rate

# Filter spike data to the selected time range
spike_mask = (spikes['times'] >= start_time) & (spikes['times'] <= end_time)
times = spikes['times'][spike_mask]
depths = spikes['depths'][spike_mask] * 1440  # Scale depth values

# Load the video file
video_path = 'C:\Users\HugoMarques\Desktop\CHRONIC_NPX\video_2025-06-24T17_54_33.avi'
cap = cv2.VideoCapture(video_path)

# Verify video loaded successfully
if not cap.isOpened():
    raise IOError("Cannot open video file")

# Set video to start at the desired frame
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create figure with two subplots: video and raster plot
fig, (ax_video, ax_raster) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]})

# Set up the raster plot
ax_raster.scatter(times, depths, s=1, c='k')
ax_raster.set_xlim(start_time, end_time)
ax_raster.set_ylim(min(depths), max(depths))
ax_raster.set_xlabel("Time (s)")
ax_raster.set_ylabel("Depth")
red_dot, = ax_raster.plot([], [], 'ro', markersize=6)  # Time indicator

# Initialize video display
ret, frame = cap.read()
if not ret:
    raise IOError("Failed to read frame from video")

frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for matplotlib
video_im = ax_video.imshow(frame_rgb)
ax_video.axis('off')

# Create time vector for animation frames
time_vector = np.linspace(start_time, end_time, end_frame - start_frame + 1)

# Animation update function
def update(i):
    global cap
    ret, frame = cap.read()
    if not ret:
        return video_im, red_dot

    # Update video frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    video_im.set_data(frame_rgb)

    # Update time indicator on raster plot
    red_dot.set_data([time_vector[i]], [ax_raster.get_ylim()[0] - 50])
    return video_im, red_dot

# Create and display the animation
ani = animation.FuncAnimation(
    fig, update, frames=end_frame - start_frame + 1, interval=1000 / frame_rate, blit=True
)

plt.tight_layout()
plt.show()
# %%
from pathlib import Path
import tqdm
import numpy as np

import matplotlib.pyplot as plt

# imports from ibl-neuropixel: uv pip install ibl-neuropixel
import spikeglx
from ibldsp.utils import WindowGenerator
from movement.io import load_poses  # uv pip install movement
import brainbox.plot
import one.alf.io as alfio

# Define path to the electrophysiology data
CAJAL_EPHYS_PATH = Path('/mnt/s1/2025/cajal')
session_path = CAJAL_EPHYS_PATH.joinpath('55920', '2025-06-24')
sleap_file = session_path.joinpath('alf', '55920_06_24.000_video_2025-06-24T17_54_33.analysis.h5')
# Find the compressed binary file containing neural recordings
bin_file = next(session_path.rglob('*.cbin'))

# Create a reader object for the binary file
sr = spikeglx.Reader(bin_file)

# Extract digital synchronization signals from the recording
trace_digital = sr.read_sync_digital()

# %% Extract synchronization pulses from the raw ephys recording
file_time_stamps = sleap_file.with_name(sleap_file.name.replace('.analysis.h5', '.time_stamps.npy'))

if not file_time_stamps.exists():
    # Create a window generator to process the data in chunks: we do not want to load the entire dataset into memory !
    wg = WindowGenerator(ns=sr.ns, nswin=100_000, overlap=0)
    pulses = []

    # Process each chunk to detect rising edges (pulses) in the sync channel
    for first, last in tqdm.tqdm(wg.firstlast, total=wg.nwin):
        sync = sr[first:last, -1]  # Get the sync channel data
        pulses.append(np.where(np.diff(sync) > 0)[0] + first)  # Detect rising edges and store their indices

    # Combine all detected pulses into a single array
    all_pulses = np.concatenate(pulses)
    # Calculate the total duration of the recording in seconds
    print((all_pulses[-1] - all_pulses[0]) / sr.fs)

    np.save(file_time_stamps, all_pulses)
else:
    all_pulses = np.load(file_time_stamps)

# %% Now relate to the behaviour data
# Load animal pose tracking data from SLEAP analysis file
ds = load_poses.from_file(
    sleap_file,
    source_software="SLEAP", 
    fps=25
)
position = ds.position
# Average positions across all tracked individuals
combined_data = position.mean(dim="individuals", skipna=True)
# Extract x,y coordinates
xy = np.nanmean(combined_data, axis=2)

# %% Load the spike sorting data

spikes = alfio.load_object(session_path.joinpath('alf'), 'spikes')
clusters = alfio.load_object(session_path.joinpath('alf'), 'clusters')
channels = alfio.load_object(session_path.joinpath('alf'), 'channels')

# %%
fig, axs = plt.subplots(3, 1, figsize=(16, 9), sharex='col', gridspec_kw={'height_ratios': [0.2, 0.2, 1]})
# Display raster map for all units
brainbox.plot.driftmap(spikes['times'], spikes['depths'] * 1440, t_bin=0.1, ax=axs[2])
# Plot X and Y position over time
axs[0].plot(all_pulses / sr.fs, xy[:-1, 0], label='x position')
axs[0].plot(all_pulses / sr.fs, xy[:-1, 1], label='y position')
# Plot velocity (change in position)
axs[1].plot(all_pulses / sr.fs, np.diff(xy[:, 0]), label='x velocity')
axs[1].plot(all_pulses / sr.fs, np.diff(xy[:, 1]), label='y velocity')
# Set axis limits
axs[2].set_xlim(350, 450)  # Focus on a specific time window
axs[1].set_ylim(-15, 15)  # Limit velocity range
axs[0].legend()
axs[1].legend()
# Save the figure
fig.savefig(session_path.joinpath('preycap_plot.png'), dpi=150)

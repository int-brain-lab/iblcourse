##
# Load the data

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from iblcourse.sources.neural_course.scripts.viewephys_model import LoadData, ViewSpikeModel

LOCAL_DATA_PATH = Path('/Users/gaelle/Documents/Work/EphysAtlas/Data')
pid = '5d570bf6-a4c6-4bf1-a14b-2c878c84ef0e'
time0 = 1500

data = LoadData(LOCAL_DATA_PATH, pid, time0)

##
# Select a channel, and get the voltage trace
indx_row = 274
single_row = data.ap[indx_row, :]

##
# Set a threshold for spike detection
threshold = -40 * 1e-6  # Change 40 to 20 for comparison
# Create two vectors, and find where threshold is crossed
vector1 = single_row[0:-2]
vector2 = single_row[1:-1]
index_cross = np.where((vector1 >= threshold) & (vector2 < threshold))[0]
print(f'{len(index_cross)} spikes detected')
##
# Plot the whole trace
t_vector = np.arange(0, len(single_row)) * 1000 / data.fs_ap
plt.plot(t_vector, single_row)
plt.hlines(threshold, t_vector[0], t_vector[-1])
plt.plot(t_vector[index_cross], single_row[index_cross], 'xr')

##
# Instantiate viewephys
ae = ViewSpikeModel(LOCAL_DATA_PATH, pid, time0)
# Plot the main GUI window
ae.view()
# Add your spikes
ae.plot_index(index_cross, channel=indx_row)
##
# Plot spike waveform

# Select a detected spike at random ; A good example spike is i_spk = 141
i_spk = np.random.randint(len(index_cross))  # This can go up to the length of index_cross
# Define a time window to plot from the threshold crossing value
time_plot = np.array([-1., 1.]) + t_vector[index_cross[i_spk]]  # -2 to 4 milliseconds from the crossing
# Get the epoch from the voltage trace
index_plot = (time_plot * data.fs_ap / 1000).astype('int')
single_row_window = single_row[index_plot[0]:index_plot[1]]
# Recompute the time at which we start plotting
t_actual = index_plot * 1000 / data.fs_ap  # in milliseconds
# Compute a time vector for plotting, of the same size as our matrix
t_vector_window = np.linspace(t_actual[0], t_actual[1], num=len(single_row_window))

# Plot
plt.plot(t_vector_window, single_row_window)
plt.xlabel('Time in recording (ms)')
plt.ylabel('Voltage (V)')

plt.hlines(threshold, t_vector_window[0], t_vector_window[-1])

plt.show()
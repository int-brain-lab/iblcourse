##
# Load the data

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from iblcourse.sources.neural_course.scripts.viewephys_model import LoadData, ViewSpikeModel
from neurodsp.waveforms import compute_spike_features, plot_peaktiptrough

LOCAL_DATA_PATH = Path('/Users/gaelle/Documents/Work/EphysAtlas/Data')
pid = '5d570bf6-a4c6-4bf1-a14b-2c878c84ef0e'
time0 = 1500

data = LoadData(LOCAL_DATA_PATH, pid, time0)

##
# Compute the features, add in the acronyms
df = compute_spike_features(data.waveforms)
df['acronym'] = data.spikes.acronym

##
# Plot the largest waveforms (positive and negative)
iw_pos = df['peak_val'].idxmax()
iw_neg = df['peak_val'].idxmin()

fig, ax = plt.subplots(2, 1)
plot_peaktiptrough(df, data.waveforms, ax=ax[0], nth_wav=iw_pos)
plot_peaktiptrough(df, data.waveforms, ax=ax[1], nth_wav=iw_neg)
ax[0].set_title(f'Wav # {iw_pos} in {data.spikes.acronym[iw_pos]}')
ax[1].set_title(f'Wav # {iw_neg} in {data.spikes.acronym[iw_neg]}')

##
# Plot half peak duration
df.groupby('acronym')['half_peak_duration'].plot(kind='kde')  # KDE: kernel density estimate
# Add label on x-axis
plt.xlabel('Peak val')  # Pandas uses matplotlib under the hood to plot
# Add legends for the curves (acronyms)
plt.legend(df.groupby('acronym').acronym.dtype.index.to_list(), title='Acronyms')

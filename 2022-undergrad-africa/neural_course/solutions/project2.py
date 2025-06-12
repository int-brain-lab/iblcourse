##
# Load the data
import numpy as np
import matplotlib.pyplot as plt
from iblcourse.sources.neural_course.scripts.viewephys_model import LoadData, ViewSpikeModel
from neurodsp.waveforms import compute_spike_features, plot_peaktiptrough
from neural_course.scripts.data_download import LOCAL_DATA_PATH

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
plt.show()

##
# Plot half peak duration
df.groupby('acronym')['half_peak_duration'].plot(kind='kde')  # KDE: kernel density estimate
# Add label on x-axis
plt.xlabel('Peak val')  # Pandas uses matplotlib under the hood to plot
# Add legends for the curves (acronyms)
plt.legend(df.groupby('acronym').acronym.dtype.index.to_list(), title='Acronyms')
plt.show()

##
# Get extreme  spikes ; Note that we make a deep copy to later amend the dataframe
df_extreme = df.loc[(df['peak_val'] < df['peak_val'].quantile(q=0.01)) |
                    (df['peak_val'] > df['peak_val'].quantile(q=0.99))].copy()

##
# Plot where are extreme spikes using viewephys GUI
sample_ext = data.spikes['sample'][df_extreme.index]
trace_ext = data.spikes['trace'][df_extreme.index]
print(f'Extreme spikes are on {len(np.unique(trace_ext))} channels')

# Instantiate viewephys
ae = ViewSpikeModel(LOCAL_DATA_PATH, pid, time0)
# Plotting the main GUI window
ae.view()
# Remove pink spikes
ae.eqcs['ap'].ctrl.remove_layer_from_label('spikes')
# Add your spikes
ae.plot_index(sample_ext, channel=trace_ext)


##
# Plot the distribution (using box plot) of half-peak duration for extreme spikes
# with either positive or negative peak value

# Create a new column
df_extreme['pos_or_neg'] = np.where(df_extreme['peak_val'] > 0, 'Positive', 'Negative')
# Box plot
df_extreme.plot.box(column="half_peak_duration", by="pos_or_neg")
plt.show()

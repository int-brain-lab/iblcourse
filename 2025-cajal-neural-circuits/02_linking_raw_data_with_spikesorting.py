from pathlib import Path
import sys

import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import matplotlib

from viewephys.gui import viewephys
import spikeglx
import one.alf.io as alfio
from iblatlas.regions import BrainRegions
from ibldsp.waveforms import double_wiggle
from ibldsp.waveforms import get_waveforms_coordinates

matplotlib.use('Qt5Agg')

regions = BrainRegions()

if sys.platform == 'win32':
    # Windows paths
    np1_data = Path(r'C:\Users\TeachingLab\Documents\Cajal2025\2025-06-15_spike-sorting-IBL\data\cajal\np1')
    np2_data = Path(r'C:\Users\TeachingLab\Documents\Cajal2025\2025-06-15_spike-sorting-IBL\data\cajal\np2')
else:
    # macOS or Linux paths
    np1_data = Path.home().joinpath('Documents/Cajal2025/2025-06-15_spike-sorting-IBL/data/cajal/np1')
    np2_data = Path.home().joinpath('Documents/Cajal2025/2025-06-15_spike-sorting-IBL/data/cajal/np2')

ap_file = next(np1_data.joinpath('raw_ephys_data').glob('*ap*.*bin'))
sr_ap = spikeglx.Reader(ap_file)

ss_path = np1_data.joinpath('spikesorting')
spikes = alfio.load_object(ss_path, 'spikes')
clusters = alfio.load_object(ss_path, 'clusters')
channels = alfio.load_object(ss_path, 'channels')
waveforms = alfio.load_object(ss_path, 'waveforms', attribute=['templates'])


# %%
# Load the raw data snippet and destripe it
CHUNK_OFFSET = 1699
t0 = 0  # Seconds in the recording
s0 = int(sr_ap.fs * t0)
dur = int(0.2 * sr_ap.fs)
raw_ap = sr_ap[s0:s0 + dur, :-sr_ap.nsync].T
butter_kwargs = {'N': 3, 'Wn': 300 / sr_ap.fs * 2, 'btype': 'highpass'}
sos = scipy.signal.butter(**butter_kwargs, output='sos')
butt = scipy.signal.sosfiltfilt(sos, raw_ap)

s0 = int(CHUNK_OFFSET * sr_ap.fs)  # This is the start of the chunk in samples
slice_spikes = slice(*np.searchsorted(spikes.samples, [s0, s0 + dur]))

ss = (spikes.samples[slice_spikes] - s0) / sr_ap.fs
cluster_attribute = clusters['metrics']['bitwise_fail'] != 0
color_map = np.array([[0, 255 , 0, 255], [255, 0, 0, 255]]).astype(np.uint8)
brush = color_map[cluster_attribute[spikes.clusters[slice_spikes]].astype(int), :]
eqc = viewephys(butt, sr_ap.fs, title='Butterworth high-pass filtered', channels=channels, t0=t0, t_scalar=1, br=regions)
eqc.ctrl.add_scatter(ss, clusters.channels[spikes.clusters[slice_spikes]],
                     label='spikes', rgb=(0, 255, 0, 100))#, brush=brush)

wrc, winds = get_waveforms_coordinates(
    clusters.channels[spikes.clusters[slice_spikes]], extract_radius_um=200, return_indices=True)  # (nw, ntrw)

ZERO_SAMPLE = 41  # this is the sample that contains the peak amplitude in the waveforms
NSW = waveforms['templates'].shape[2]

# %%
scatter_item = eqc.layers['spikes']['layer']

def on_click(plot, points):

    for point in points:
        index = point.index()

        idx_spike = slice_spikes.start + index
        clicked_cluster = spikes.clusters[idx_spike]

        # Find all spikes of the clicked cluster in the current view
        cluster_mask = spikes.clusters[slice_spikes] == clicked_cluster
        cluster_times = (spikes.samples[slice_spikes][cluster_mask] - s0) / sr_ap.fs
        cluster_channels = clusters.channels[spikes.clusters[slice_spikes]][cluster_mask]

        # Sort the points by time
        sort_indices = np.argsort(cluster_times)
        cluster_times = cluster_times[sort_indices]
        cluster_channels = cluster_channels[sort_indices]

        # Create a new line item
        my_scatter = eqc.ctrl.add_scatter(cluster_times, cluster_channels, label='cluster_scatter', rgb=(250, 0, 250, 180))
        # Set a lower zValue to make it appear under previous plots
        print(f"Clicked cluster: {clicked_cluster}")
        print(f"Number of spikes in this cluster: {np.sum(cluster_mask)}")

        # plot the waveforms
        spike_sample = int(spikes['samples'][idx_spike]) - s0
        tsel = slice(spike_sample - ZERO_SAMPLE, spike_sample - ZERO_SAMPLE + NSW)
        raw_waveform = butt[winds[index, :], tsel]

        fig, ax = plt.subplots(2, 1, figsize=(6, 8))
        i = clicked_cluster
        double_wiggle(waveforms['templates'][i] * 1e6 / 250, clip=4, ax=ax[0], fs=sr_ap.fs)
        double_wiggle(raw_waveform * 1e6 / 250, clip=4, ax=ax[1], fs=sr_ap.fs)
        fig.show()

scatter_item.sigClicked.connect(on_click)
# %gui qt5
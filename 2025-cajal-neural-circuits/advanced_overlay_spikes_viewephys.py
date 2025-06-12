
# %%
import numpy as np
import scipy.signal
from one.api import ONE
from brainbox.io.one import SpikeSortingLoader
from iblatlas.atlas import BrainRegions
from viewephys.gui import viewephys

regions = BrainRegions()
one = ONE(mode='remote', base_url="https://alyx.internationalbrainlab.org", cache_dir="/mnt/s1/spikesorting/raw_data")  # parede cache:

pids = [
    '1a276285-8b0e-4cc9-9f0a-a3a002978724',  # Benchmark PIDS start
    '1e104bf4-7a24-4624-a5b2-c2c8289c0de7',
    '6638cfb3-3831-4fc2-9327-194b76cf22e1',
    '749cb2b7-e57e-4453-a794-f6230e4d0226',
    'd7ec0892-0a6c-4f4f-9d8f-72083692af5c',
    'da8dfec1-d265-44e8-84ce-6ae9c109b8bd',
    'dab512bd-a02d-4c1f-8dbc-9155a163efc0',
    'dc7e9403-19f7-409f-9240-05ee57cb7aea',
    'e8f9fba4-d151-4b00-bee7-447f0f3e752c',
    'eebcaf65-7fa4-4118-869d-a084e84530e2',
    'fe380793-8035-414e-b000-09bfe5ece92a',  # Benchmark PIDS stop
]
pid = 'e8f9fba4-d151-4b00-bee7-447f0f3e752c'
pid = 'fe380793-8035-414e-b000-09bfe5ece92a'
# Load spike sorting
t0 = 1800
sl = SpikeSortingLoader(pid=pid, one=one)
spikes, clusters, channels = sl.load_spike_sorting(dataset_types=['spikes.samples'])
clusters = sl.merge_clusters(spikes, clusters, channels)
waveforms = sl.load_spike_sorting_object('waveforms')

sr = sl.raw_electrophysiology(band='ap', stream=False)
raw = sr[int(t0 * sr.fs):int((t0 + 1) * sr.fs), :-sr.nsync].T

# %%
butter_kwargs = {'N': 3, 'Wn': 300 / sr.fs * 2, 'btype': 'highpass'}
sos = scipy.signal.butter(**butter_kwargs, output='sos')
butt = scipy.signal.sosfiltfilt(sos, raw)

# overlay the spikes
tprobe = spikes.samples / sr.fs
slice_spikes = slice(np.searchsorted(tprobe, t0), np.searchsorted(tprobe, t0 + 1))


eqc = viewephys(butt, sr.fs, title='Butterworth high-pass filtered', channels=channels, t0=t0, t_scalar=1, br=regions)
eqc.ctrl.add_scatter(tprobe[slice_spikes], clusters.channels[spikes.clusters[slice_spikes]], label='spikes')

# add spikes with passing in green and failing in red
cluster_attribute = clusters['bitwise_fail'] != 0
color_map = np.array([[0, 255 , 0, 255], [255, 0, 0, 255]]).astype(np.uint8)
brush = color_map[cluster_attribute[spikes.clusters[slice_spikes]].astype(int), :]
eqc.ctrl.add_scatter(tprobe[slice_spikes], clusters.channels[spikes.clusters[slice_spikes]],
                     brush=brush, label='spikes', rgb=(0, 0, 0, 0))


# %%
from ibldsp.waveforms import double_wiggle
import matplotlib.pyplot as plt
from ibldsp.waveforms import get_waveforms_coordinates  # requires ibl-neuropixel 1.8.0 or at the very least the Cajal branch

EXTRACT_RADIUS_UM = 200

wrc, winds = get_waveforms_coordinates(
    clusters.channels[spikes.clusters[slice_spikes]], extract_radius_um=200, return_complex=True, return_indices=True)  # (nw, ntrw)

ZERO_SAMPLE = 41  # this is the sample that contains the peak amplitude
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
        cluster_times = tprobe[slice_spikes][cluster_mask]
        cluster_channels = clusters.channels[spikes.clusters[slice_spikes]][cluster_mask]

        # Sort the points by time
        sort_indices = np.argsort(cluster_times)
        cluster_times = cluster_times[sort_indices]
        cluster_channels = cluster_channels[sort_indices]

        # Create a new line item
        my_scatter = eqc.ctrl.add_scatter(cluster_times, cluster_channels, label='cluster_scatter', rgb=(250, 0, 250, 180), size=12)
        # Set a lower zValue to make it appear under previous plots
        my_scatter.setZValue(0)
        print(f"Clicked cluster: {clicked_cluster}")
        print(f"Number of spikes in this cluster: {np.sum(cluster_mask)}")

        # plot the waveforms
        spike_sample = int(spikes['samples'][idx_spike]) - int(t0 * sr.fs)
        tsel = slice(spike_sample - ZERO_SAMPLE, spike_sample - ZERO_SAMPLE + NSW)
        raw_waveform = butt[winds[index, :], tsel]

        fig, ax = plt.subplots(2, 1, figsize=(6, 8))
        i = clicked_cluster
        double_wiggle(waveforms['templates'][i] * 1e6 / 250, clip=4, ax=ax[0], fs=sr.fs)
        double_wiggle(raw_waveform * 1e6 / 250, clip=4, ax=ax[1], fs=sr.fs)
        fig.show()


# scatter_item.sigClicked.disconnect(on_click)
scatter_item.sigClicked.connect(on_click)
a = 1

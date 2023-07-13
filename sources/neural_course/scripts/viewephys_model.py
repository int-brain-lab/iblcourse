import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from neurodsp.waveforms import plot_peaktiptrough, compute_spike_features
from neurodsp.utils import rms

from ibllib.atlas import BrainRegions
from ibllib.plots import wiggle
from ibllib.plots import Density

from viewephys.gui import viewephys


def plot_spike_window(wav, fs=30000, iw=None, dens_min_x=-0.00011, dens_max_x=0.00011, region=None):
    fig, axs = plt.subplots(3, 2)

    # Subplot wiggle
    wiggle(-wav, fs=fs, gain=40, ax=axs[0, 0])
    if region is not None:
        axs[0, 0].set_title(f'Spike # {iw} in {region}')
    else:
        axs[0, 0].set_title(f'Spike # {iw}')

    # Subplot with peak-tip-trough
    new_wav = wav[np.newaxis, :, :]
    df, arr_out = compute_spike_features(new_wav, return_peak_channel=True)
    plot_peaktiptrough(df, new_wav, axs[1, 0], nth_wav=0)

    # Subplot density of waveform
    d1 = Density(-wav.transpose(), fs=fs, taxis=1, ax=axs[2, 0], vmin=dens_min_x, vmax=dens_max_x, cmap='Greys')
    axs[2, 0].set_ylabel('Channels')

    # Other
    # axs[0, 1].set_visible(False)
    axs[0, 1].set_title(f'Name of the plots:')
    axs[0, 1].text(0, 1, 'Wiggle')
    axs[0, 1].axis('off')

    # axs[1, 1].set_visible(False)
    axs[1, 1].text(0, 1, 'Peak channel')
    axs[1, 1].axis('off')

    # axs[2, 1].set_visible(False)
    axs[2, 1].text(0, 1, 'Density')
    axs[2, 1].axis('off')

    fig.show()
    return fig, axs


class LoadData(object):
    def __init__(self, ROOT_PATH, pid, t0=1500):
        self.ROOT_PATH = ROOT_PATH
        self.pid = pid
        self.T0 = t0

        self.path_pid = self.ROOT_PATH.joinpath(self.pid)
        self.path_t0 = next(self.path_pid.glob(f'T0{self.T0}*'))

        self.regions = BrainRegions()

        self.ap = np.load(self.path_t0.joinpath('destriped.npy')).astype(np.float32)
        self.zscore = rms(self.ap)
        with open(self.path_t0.joinpath('ap.yml'), 'r') as f:
            ap_info = yaml.safe_load(f)
        self.fs_ap = ap_info['fs']

        spikes = pd.read_parquet(self.path_t0.joinpath('spikes.pqt'))
        self.spikes = spikes.reset_index()

        self.waveforms = np.load(self.path_t0.joinpath('waveforms.npy'))

        ch_load = np.load(self.path_t0.joinpath('channels.npy'), allow_pickle=True)
        self.channels = dict(ch_load.item())

        # Add in region acronym to spikes dataframe for simplicity for students
        self.spikes['acronym'] = self.channels['acronym'][self.spikes['trace'].to_numpy().astype('int')]


class ViewSpikeModel(LoadData):

    def __init__(self, ROOT_PATH, pid, t0=1500):

        LoadData.__init__(self, ROOT_PATH, pid, t0=t0)

        self.eqcs = {}

    def view(self, alpha_min=100):

        self.eqcs['ap'] = viewephys(self.ap, fs=self.fs_ap, title='ap', channels=self.channels, br=self.regions)
        sel = self.spikes['alpha'] > alpha_min
        self.eqcs['ap'].ctrl.add_scatter(
            self.spikes['sample'][sel] / self.fs_ap * 1e3,
            self.spikes['trace'][sel],
            (200, 0, 200, 100),
            label='spikes')

        sl = self.eqcs['ap'].layers['spikes']
        try:
            sl['layer'].sigClicked.disconnect()
        except:
            pass
        sl['layer'].sigClicked.connect(self.click_on_spike_callback)

    def click_on_spike_callback(self, obj, toto, event):
        t = event.pos().x() / 1e3
        c = int(event.pos().y())
        fs = self.fs_ap
        ispi = np.arange(
            np.searchsorted(self.spikes['sample'], int(t * fs) - 5),
            np.searchsorted(self.spikes['sample'], int(t * fs) + 5) + 1
        )
        iw = ispi[np.argmin(np.abs(self.spikes['trace'].iloc[ispi] - c))]
        print(iw)

        rwav, hwav, cind, sind = self.getwaveform(iw, return_indices=True)
        wav = np.squeeze(self.waveforms[iw, :, :] * self.zscore[cind])

        region = self.channels['acronym'][cind]
        if len(cind) > 1:
            region = region[0]

        plot_spike_window(wav, fs=self.fs_ap, iw=iw, region=region)

    def view_spike(self, iw):
        cind = int(self.spikes.trace.to_numpy()[iw])
        wav = np.squeeze(self.waveforms[iw, :, :] * self.zscore[cind])
        region = self.channels['acronym'][cind]
        plot_spike_window(wav=wav, fs=self.fs_ap, iw=iw, region=region)

    def plot_index(self, index, channel):
        self.eqcs['ap'].ctrl.add_scatter(
            index / self.fs_ap * 1e3,
            np.ones(index.shape) * channel,
            (250, 0, 0, 100),
            label='index')

    @property
    def xy(self):
        return self.channels['lateral_um'] + 1j * self.channels['axial_um']

    def getwaveform(self, iw, extract_radius=200, trough_offset=42, spike_length_samples=121, return_indices=False):
        s0 = int(self.spikes['sample'].iloc[iw] - trough_offset)
        sind = slice(s0, s0 + int(spike_length_samples))

        cind = np.abs(self.xy[int(self.spikes['trace'].iloc[iw])] - self.xy) <= extract_radius
        hwav = {k: v[cind] for k, v in self.channels.items()}
        if return_indices:
            return self.ap[cind, sind], hwav, cind, sind
        else:
            return self.ap[cind, sind], hwav

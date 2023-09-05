'''
Prepare data for viewephys course
'''
##
'''
Instanciate PID, PATH and ONE 
'''
from pathlib import Path
from one.api import ONE
import numpy as np
from brainbox.io.spikeglx import Streamer
from neurodsp.voltage import destripe
from one.remote import aws
from brainbox.io.one import SpikeSortingLoader

LOCAL_DATA_PATH = Path.home().joinpath('iblcourse', 'neural_course', 'data')
LOCAL_DATA_PATH.mkdir(parents=True, exist_ok=True)
one = ONE(base_url='https://alyx.internationalbrainlab.org')

pid = '5d570bf6-a4c6-4bf1-a14b-2c878c84ef0e'
time0 = 1500  # timepoint in recording to stream  # TODO: When selecting 500 it not work as folder name requires 0500

local_data_path_pid_t0 = LOCAL_DATA_PATH.joinpath(pid).joinpath(f'T0{time0}')
##
'''
Download waveform and raw data:
https://github.com/int-brain-lab/paper-ephys-atlas/blob/main/sources/examples/01_download-ephys-atlas-samples.py
'''
if not local_data_path_pid_t0.exists():
    s3, bucket_name = aws.get_s3_from_alyx(alyx=one.alyx)
    aws.s3_download_folder(f"resources/ephys-atlas-sample/{pid}/T0{time0}", local_data_path_pid_t0, s3=s3,
                           bucket_name=bucket_name)

##
# Re-create shortened (1s) destripe data and save
time_win = 1  # number of seconds to stream
band = 'ap'  # either 'ap' or 'lf'

sr = Streamer(pid=pid, one=one, remove_cached=False, typ=band)
s0 = time0 * sr.fs
tsel = slice(int(s0), int(s0) + int(time_win * sr.fs))

# Important: remove sync channel from raw data, and transpose
raw = sr[tsel, :-sr.nsync].T

# Apply destriping algorithm to data
destriped = destripe(raw, fs=sr.fs)
np.save(local_data_path_pid_t0.joinpath('destriped.npy'), destriped)

##
# Load channels data
ssl = SpikeSortingLoader(pid=pid, one=one)
channels = ssl.load_channels()
np.save(local_data_path_pid_t0.joinpath('channels.npy'), channels)
# # re-load
# ch_load = np.load(local_data_path_pid_t0.joinpath('channels.npy'), allow_pickle=True)
# channels = dict(ch_load.item())

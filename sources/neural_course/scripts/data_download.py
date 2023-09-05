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

pids = [  # http://benchmarks.internationalbrainlab.org.s3-website-us-east-1.amazonaws.com/#/0/4
    '1a276285-8b0e-4cc9-9f0a-a3a002978724',
    '1e104bf4-7a24-4624-a5b2-c2c8289c0de7',
    '5d570bf6-a4c6-4bf1-a14b-2c878c84ef0e',
    '5f7766ce-8e2e-410c-9195-6bf089fea4fd',
    '6638cfb3-3831-4fc2-9327-194b76cf22e1',
    '749cb2b7-e57e-4453-a794-f6230e4d0226',
    'd7ec0892-0a6c-4f4f-9d8f-72083692af5c',
    'da8dfec1-d265-44e8-84ce-6ae9c109b8bd',
    'dab512bd-a02d-4c1f-8dbc-9155a163efc0',
    'dc7e9403-19f7-409f-9240-05ee57cb7aea',
    'e8f9fba4-d151-4b00-bee7-447f0f3e752c',
    'eebcaf65-7fa4-4118-869d-a084e84530e2',
    'fe380793-8035-414e-b000-09bfe5ece92a',
]

pid = pids[1]
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

'''
THIS SCRIPT REQUIRES mayavi AND iblapps
Please use iblenv to run it

Neural course
Plot the trajectories of the 3 selected PID in 3D
'''
import numpy as np
import pandas as pd
from iblatlas.atlas import NeedlesAtlas, AllenAtlas, Insertion
from one.api import ONE
from pathlib import Path
from ibllib.pipes.histology import interpolate_along_track
from mayavi import mlab
from iblapps.atlaselectrophysiology import rendering

one = ONE()

needles = NeedlesAtlas()
ba = AllenAtlas(25)
allen = AllenAtlas()
ba.compute_surface()

pids = ['1a276285-8b0e-4cc9-9f0a-a3a002978724',
        '5d570bf6-a4c6-4bf1-a14b-2c878c84ef0e',
        'da8dfec1-d265-44e8-84ce-6ae9c109b8bd']

# Download table of features
path_features = Path('/Users/gaelle/Documents/Work/EphysAtlas/channels.pqt')
channels = pd.read_parquet(path_features)


def from_ins_xyz_ccf(ins, pid, channels):
    txyz = np.flipud(ins.xyz)
    txyz = allen.bc.i2xyz(needles.bc.xyz2i(txyz / 1e6, round=False, mode="clip")) * 1e6
    # we interploate the channels from the deepest point up. The neuropixel y coordinate is from the bottom of the probe
    xyz_mm = interpolate_along_track(txyz, channels.loc[pid, 'axial_um'].to_numpy() / 1e6)
    xyz_cff = ba.xyz2ccf(xyz_mm)
    return xyz_cff


##
fig = rendering.figure()
for pid in pids:
    # From Alyx (this gives in BA as input)
    trj = one.alyx.rest('trajectories', 'list', probe_insertion=pid, provenance='Ephys aligned histology track')[0]
    ins_trj = Insertion.from_dict(trj, brain_atlas=ba)
    xzy_trj = from_ins_xyz_ccf(ins_trj, pid, channels)

    # Plot
    color = (0.2, 0.2, 0.2)  # Black
    mlab.points3d(xzy_trj[:, 1], xzy_trj[:, 2], xzy_trj[:, 0],
                  color=color)

    # set text
    text_str = pid[0:8]
    mlab.text3d(xzy_trj[-1, 1], xzy_trj[-1, 2], xzy_trj[-1, 0] - 500, text_str,
                line_width=4, color=color, figure=fig, scale=300)
##
# ADJUST BY HAND THEN SAVE
mlab.savefig('/Users/gaelle/Documents/Git/int-brain-lab/iblcourse/sources/neural_course/images/3_pids.png')

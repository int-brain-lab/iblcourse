'''
Neural course
Plot the trajectories of the 3 selected PID in 3D
'''
import numpy as np
import pandas as pd
from ibllib.atlas import NeedlesAtlas, AllenAtlas, Insertion
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

pids = ['1e104bf4-7a24-4624-a5b2-c2c8289c0de7',
        '5d570bf6-a4c6-4bf1-a14b-2c878c84ef0e',
        '6638cfb3-3831-4fc2-9327-194b76cf22e1']

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
    mlab.points3d(xzy_trj[:, 1], xzy_trj[:, 2], xzy_trj[:, 0],
                  color=(0.2, 0.2, 0.2))  # Black


mlab.savefig('/Users/gaelle/Documents/Git/int-brain-lab/ibldevtools/Gaelle/courses/images/3_pids.png')

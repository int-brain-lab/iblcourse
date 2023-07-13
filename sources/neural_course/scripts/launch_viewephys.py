##
import numpy as np
from pathlib import Path
from iblcourse.sources.neural_course.scripts.viewephys_model import ViewSpikeModel, LoadData

LOCAL_DATA_PATH = Path('/Users/gaelle/Documents/Work/EphysAtlas/Data')
pid = '5d570bf6-a4c6-4bf1-a14b-2c878c84ef0e'
time0 = 1500

##
# Instantiate viewephys
ae = ViewSpikeModel(LOCAL_DATA_PATH, pid, time0)
# Plotting the main GUI window
ae.view()

##
# Plotting just the pop-up window for a given spike
ae.view_spike(iw=2284)
# Adding some spike indices
ae.plot_index(np.array([0, 23, 32, 422]), channel=299)

##
# Load only the data
data = LoadData(LOCAL_DATA_PATH, pid, time0)

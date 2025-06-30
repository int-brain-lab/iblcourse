# here we will launch the spike sorting process using IBL Sorter: https://github.com/int-brain-lab/ibl-sorter
from pathlib import Path
from iblsorter.ibl import run_spike_sorting_ibl, ibl_pykilosort_params

# Set the directory where IBL Sorter will store temporary files
SCRATCH_DIR = Path.home().joinpath('scratch', 'iblsorter')
# Set up the input and output paths
bin_file = Path('/mnt/s1/2025/cajal/sample/55920_NPX_5_g0_t0.imec0.ap.bin')  # done !
bin_file = Path('/mnt/s1/2025/cajal/20250625_55920_NPX_g0_imec0/20250625_55920_NPX_g0_t0.imec0.ap.bin') # done !
bin_file = Path('/mnt/s1/2025/cajal/55920_NPX_g0/55920_NPX_g0_imec0/55920_NPX_g0_t0.imec0.ap.bin') # running
bin_file = Path('/mnt/s1/2025/cajal/55840_NPX_g0/55840_NPX_g0_imec0/55840_NPX_g0_t0.imec0.ap.bin')  # todo
OUTPUT_DIR = bin_file.parent.joinpath('sorting_output')

# here we initialize the IBL Sorter parameters for the spike sorting process
params = ibl_pykilosort_params(bin_file)
# we set the PSD high-frequency threshold to a very high value because we have high-frequency noise in the data
params.channel_detection_parameters.psd_hf_threshold = 1e6
# additionally, we add a high-frequency cutoff to further reduce high-frequency noise
params.fslow = 9_000

# finally, we run the spike sorting process using the provided parameters
run_spike_sorting_ibl(
    bin_file,
    scratch_dir=SCRATCH_DIR,
    params=params,
    ks_output_dir=OUTPUT_DIR.joinpath('iblsorter'),
    alf_path=OUTPUT_DIR.joinpath('alf'),
    extract_waveforms=True
)

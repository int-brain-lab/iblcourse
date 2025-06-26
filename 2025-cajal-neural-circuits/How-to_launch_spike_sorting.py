# The following requires iblsorter >= 1.9.1
# https://github.com/int-brain-lab/ibl-sorter

from pathlib import Path
from iblsorter.ibl import run_spike_sorting_ibl, ibl_pykilosort_params
SCRATCH_DIR = Path.home().joinpath('scratch', 'iblsorter')

bin_file = Path('/mnt/s1/2025/cajal/sample/55920_NPX_5_g0_t0.imec0.ap.bin')  # done !
bin_file = Path('/mnt/s1/2025/cajal/20250625_55920_NPX_g0_imec0/20250625_55920_NPX_g0_t0.imec0.ap.bin') # done !
bin_file = Path('/mnt/s1/2025/cajal/55920_NPX_g0/55920_NPX_g0_imec0/55920_NPX_g0_t0.imec0.ap.bin') # running
bin_file = Path('/mnt/s1/2025/cajal/55840_NPX_g0/55840_NPX_g0_imec0/55840_NPX_g0_t0.imec0.ap.bin')  # todo

OUTPUT_DIR = bin_file.parent.joinpath('sorting_output')
params = ibl_pykilosort_params(bin_file)
params.channel_detection_parameters.psd_hf_threshold = 1e6
params.fslow = 9_000
run_spike_sorting_ibl(
    bin_file,
    scratch_dir=SCRATCH_DIR,
    params=params,
    ks_output_dir=OUTPUT_DIR.joinpath('iblsorter'),
    alf_path=OUTPUT_DIR.joinpath('alf'),
    extract_waveforms=True
)

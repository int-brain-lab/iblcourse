# %%
# the uncompressed dataset size is 193 Gb, lets compress the raw electrophysiology bin files to save disk space and speed up transfers
# with NP2, the compressed to uncompressed ratio is around 60%.

from pathlib import Path
import spikeglx

CAJAL_EPHYS_PATH = Path('/mnt/s1/2025/cajal')
for bin_file in CAJAL_EPHYS_PATH.rglob('*.bin'):
    sr = spikeglx.Reader(bin_file)
    print(sr.file_bin, sr.nbytes / 1024 ** 3, 'Gb')
    # this will remove the original file and save a compressed version, but only after a full read after write sample to sample check
    sr.compress_file(keep_original=False)

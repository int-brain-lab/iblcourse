# Course Materials

- [Outline and links to presentations](https://docs.google.com/document/d/1ztWzAopXW6agdEt3ub5Jkn3mmSZG5CqaO2e0jQT39yQ/edit?tab=t.0)
- [Datasets](https://ibl-brain-wide-map-public.s3.amazonaws.com/index.html#sample_data/cajal)



# Installation

macOS and Linux
```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
uv venv iblenv
uv pip install ibllib
uv pip install viewephys
uv pip install ipython
```

Windows
```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Restart powershell and then:
```
uv python install 3.12

New-Item -Path "C:\Users\TeachingLab\Documents\Cajal2025\2025-06-15_spike-sorting-IBL" -ItemType Directory -Force
cd C:\Users\TeachingLab\Documents\Cajal2025\2025-06-15_spike-sorting-IBL

uv venv iblenv
uv pip install ibllib
uv pip install viewephys
uv pip install ipython
```

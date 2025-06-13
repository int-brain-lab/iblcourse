# Course Materials

- [Outline and links to presentations](https://docs.google.com/document/d/1ztWzAopXW6agdEt3ub5Jkn3mmSZG5CqaO2e0jQT39yQ/edit?tab=t.0)
- [Datasets](https://ibl-brain-wide-map-public.s3.amazonaws.com/index.html#sample_data/cajal)

# Getting Started

```shell
cd C:\Users\TeachingLab\Documents\Cajal2025\2025-06-15_spike-sorting-IBL
.\iblenv\Scripts\Activate.ps1  # activate environment
jupyter lab
```

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

Restart powershell and then install Python, setup the environment and dependencies
```shell
# install Python 3.12
uv python install 3.12  
# create our working directory if needed
New-Item -Path "C:\Users\TeachingLab\Documents\Cajal2025\2025-06-15_spike-sorting-IBL" -ItemType Directory -Force
cd C:\Users\TeachingLab\Documents\Cajal2025\2025-06-15_spike-sorting-IBL
# allow activation of environment (love it)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# create environment
uv venv iblenv
# activate environment
.\iblenv\Scripts\Activate.ps1
# install dependencies
uv pip install ibllib viewephys jupyterlab
```

Download the course material: lectures and data
```shell
cd C:\Users\TeachingLab\Documents\Cajal2025\2025-06-15_spike-sorting-IBL
# this will get the code material and lectures
git clone https://github.com/int-brain-lab/iblcourse.git
# download and unzip the dataset
Invoke-WebRequest -Uri "https://ibl-brain-wide-map-public.s3.us-east-1.amazonaws.com/sample_data/cajal/cajal.zip" -OutFile "cajal.zip"
Expand-Archive -Path "cajal.zip" -DestinationPath ".\cajal_data" -Force
```
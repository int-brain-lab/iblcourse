# About
This repository contains 

# Installation

## Before starting:  Learn to use the terminal
You will need to be familiar with the terminal, a native program on your machine that helps you run commands. 
Learn how to launch it, as well as useful commands (we will mainly use the `pip` command) via this reference:
- [Learning how to use the terminal](https://realpython.com/terminal-commands/)

## Before starting:  Install Anaconda and Git
Install Anaconda and Git, selecting the packages depending on your OS (Max, Windows or Linux):
- [Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html)
- [Git](https://git-scm.com/downloads)

## Begin the installation
Once you are familiarised with the terminal, do the steps below.

### Clone the repository
- Create a folder on your machine called `int-brain-lab`
- Open a terminal, and navigate to this folder using `cd`, e.g. `cd Documents/Git/int-brain-lab/` 
- Then type:
```
git clone https://github.com/int-brain-lab/iblcourse.git
```

### Setup your python environment
Either create a new environment `coursenv` and activate it:
- In the terminal, type in the following commands:

```
conda create --name coursenv python=3.10 --yes
conda activate coursenv
```

or activate the [environment `iblenv`](https://github.com/int-brain-lab/iblenv/blob/master/README.md) if already installed.

### Install the necessary packages
Once your environment is activated, type in the terminal the following command:
```
pip install -e .
```

This will install:
- [viewephys](https://github.com/int-brain-lab/viewephys#installation )
- other dependencies necessary: [ibl-neuropixel](https://github.com/int-brain-lab/ibl-neuropixel/tree/main) and [ibllib](https://github.com/int-brain-lab/ibllib)

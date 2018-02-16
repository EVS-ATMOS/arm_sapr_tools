#!/bin/bash
#adapted from Py-ART's Thanks Jonathan Helmus!
set -e
# use next line to debug this script
#set -x

# Install Miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O miniconda.sh
chmod +x miniconda.sh
./miniconda.sh -b
export PATH=/home/travis/miniconda3/bin:$PATH
export COIN_INSTALL_DIR=/home/travis/miniconda3/envs/testenv
conda config --set always_yes yes
conda config --set show_channel_urls true
conda update -q conda

## Create a testenv with the correct Python version
conda env create -f continuous_integration/environment-$PYTHON_VERSION.yml
source activate testenv

# install Py-ART
export RSL_PATH=~/miniconda3/envs/testenv
python setup.py build_ext --inplace
pip install -ve .

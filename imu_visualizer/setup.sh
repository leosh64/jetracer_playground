#!/usr/bin/env bash

# exit when any command fails
set -e

# *** SETTINGS ***
PYTHON_VENV_DIR=".venv"

install_package_if_not_present() {
    REQUIRED_PKG=$1
    PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed" || true)
    echo "Checking for $REQUIRED_PKG: $PKG_OK..."
    if [ "" = "$PKG_OK" ]; then
    echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
    sudo apt-get install --yes $REQUIRED_PKG
    fi
}

install_package_if_not_present python3-venv
install_package_if_not_present git

# all these are required for pygame-2
sudo apt-get install --yes libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev python3-setuptools python3-dev python3 libportmidi-dev

echo "Removing old python venv, if exists..."
if [ -d "$PYTHON_VENV_DIR" ]; then
    # rm -rf $WORKING_DIR; # TODO: put back in
    echo "do something"
fi

echo "Creating python venv..."
python3 -m venv $PYTHON_VENV_DIR

echo "Activating python venv..."
source $PYTHON_VENV_DIR/bin/activate

echo "Upgrading python pip..."
python3 -m pip install --upgrade pip

echo "Installing required python packages..."
pip3 install wheel
pip3 install -r requirements.txt

echo "Getting madgwick_py package from Github..."
git clone git@github.com:morgil/madgwick_py.git

echo "Activate python venv with $PYTHON_VENV_DIR/bin/activate"

#!/bin/bash -e
# Create or replace the app's python virtual environment and installs all the packages required for the app.
#
# Usage:
#
# ./install_package.sh


script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VIRTUAL_ENV_PATH="${VIRTUAL_ENV_PATH:=${script_dir}/virtual_env}"

requirements_pip_file="${REQUIREMENTS_PIP_FILE:-requirements.txt}"

# Create or replace python virtual environment
echo "Creating/Replacing VirtualEnv"
rm -rf $VIRTUAL_ENV_PATH
mkdir -p "${VIRTUAL_ENV_PATH}" 2>/dev/null

if PYTHON3_PATH=$(which python3); then
    virtualenv --python=$PYTHON3_PATH $VIRTUAL_ENV_PATH
else
    echo "Could not find Python 3 on system. Please install it."
    exit 1
fi

# Install the package and its dependencies
echo "Installing pip requirement file: ${requirements_pip_file}"
./run_in_venv.sh pip install -r "${requirements_pip_file}"

echo "Setup.py Installing"
./run_in_venv.sh python setup.py install

#!/bin/bash

# Runs any command in the application's python virtual environment. This script assumes
# the environment has been installed using install_miniconda.sh and
# install_app.sh.
#
# Usage:
# ./run_in_environment.sh python setup.py test
#
# You can also use it to activate the virtual environment, e.g.:
# source run_in_environment.sh
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

VIRTUAL_ENV_PATH="${VIRTUAL_ENV_PATH:=${script_dir}/virtual_env}"
ACTIVATE_FILE="${VIRTUAL_ENV_PATH}/bin/activate"

# Get out of currently activate venvs, if any
if [[ $VIRTUAL_ENV ]]; then
    deactivate 2> /dev/null
fi

if [ -f $ACTIVATE_FILE ]; then
    source $ACTIVATE_FILE
    exec "$@"
else
    echo "Error: the file $ACTIVATE_FILE does not exist. Please install the environment correctly."
    # Only exit if you're not in an interactive session
    if [[ $- != *"i"* ]] ; then exit 1 ; fi
fi

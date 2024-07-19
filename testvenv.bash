#!/usr/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

QUIVER_ROOT=`dirname "$(realpath $0)"`
USER=`whoami`
USER_HOME=/home/$USER
APACHE_ROOT=/etc/apache2
PYTHON_EXEC=`which python3`

BACKGROUND_BBLUE="\u001b[44;1m"
BACKGROUND_END="\u001b[0m"

function createVirtualEnv() {
    echo ""
    echo "${bold}►►► Creating Quiver Virtual Environment${normal}"
    virtualenv -p $PYTHON_EXEC .quiverenv
}

createVirtualEnv

echo ""
echo "${bold}►►► Global modules${normal}"
python3 -m pip list

source .quiverenv/bin/activate

echo ""
echo "${bold}►►► .quiverenv modules${normal}"
python3 -m pip list

deactivate

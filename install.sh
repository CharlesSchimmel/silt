#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo "You must be root to install this script." 1>&2
    exit 1
else
    echo "Checking/Installing Pip3"
    apt-get install pip3
    echo "Checking/Installing Requests"
    pip3 install requests
    cp silt.py /usr/bin/silt
    cp silt.ini $HOME/.config/silt.ini
    echo "Done. Enter 'silt' to run."
    echo "Config located at $HOME/.config/silt.ini"
    exit 1
fi

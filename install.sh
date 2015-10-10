#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo "You must be root to install this script." 1>&2
    exit 1
else
    echo "Checking/Installing Pip3"
    if ! pip3 >/dev/null 2>&1; then
        echo "pip3 not found, attempting to install:"
        if apt >/dev/null 2>&1; then
            apt-get install python3.4 python3-pip
        else
            echo "apt-get currently the only supported package manager. Please install pip3 seperately."
        fi
    fi
    echo "Checking/Installing Requests via pip3"
    pip3 install requests
    cp -p silt.py /usr/bin/silt
    cp -p silt.ini $HOME/.config/silt.ini
    echo "Done. Enter 'silt' to run."
    echo "Config located at $HOME/.config/silt.ini"
    exit 1
fi

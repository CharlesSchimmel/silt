#!/bin/bash

CONFIG=$HOME/.config/silt.ini

if [ "$(id -u)" != "0" ]; then
    echo "You must be root to install this script." 1>&2
    exit 1
else
    echo "This will install 'silt.'"
    echo "[ENTER] to confirm"
    read confirm
    echo "Checking/Installing Pip3"
        if ! pip3 >/dev/null 2>&1; then
            echo "pip3 not found, attempting to install:"
            if apt >/dev/null 2>&1; then
                apt-get install python3.4 python3-pip
            else
                echo "apt currently the only supported package manager. Please install pip3 seperately."
            fi
        fi
        echo "Checking/Installing Requests via pip3"
        pip3 install requests
        cp -p silt.py /usr/bin/silt
        if ! [ -e $CONFIG ]; then
            echo "Copying config..."
            cp -p silt.ini $CONFIG
        fi
        echo "Done. Enter 'silt' to run."
        echo "Config located at $HOME/.config/silt.ini"
fi

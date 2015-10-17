#!/bin/bash

APP=$HOME/.silt/
CONFIG=$APP/silt.ini
BINLOC=/usr/local/bin/silt

if [ "$(id -u)" != "0" ]; then
    echo "You must be root to install this script." 1>&2
    exit 1
else
    echo "This will install 'silt' and its dependency 'requests' via pip3.'"
    echo "[ENTER] to confirm"
    read confirm
    echo "Checking/Installing Pip3"
        if ! pip3 >/dev/null 2>&1; then
            echo "pip3 not found, attempting to install:"
            if apt >/dev/null 2>&1; then
                apt-get install python3.4 python3-pip
            else
                echo "apt currently the only supported package manager. Please install pip3 and requests seperately."
            fi
        fi
        echo "Checking/Installing Requests via pip3"
        pip3 install requests

        #check if app location exists; only make it if it exists
        if ! [ -e $APP ]; then
            mkdir -m 777 $APP
        fi

        #cp will overwrite
        cp -p silt.py $APP/silt.py

        #if there's already something in the bin location, delete it
        if [ -e $BINLOC ]; then
            rm $BINLOC
        fi
        #make a softlink from the app location to the bin location
        ln -s $APP/silt.py /usr/local/bin/silt

        if ! [ -e $CONFIG ]; then
            echo "Copying config..."
            cp -p silt.ini $CONFIG
        fi

        echo "Done. Enter 'silt' to run."
        echo "Config located at $HOME/.silt/silt.ini"
fi

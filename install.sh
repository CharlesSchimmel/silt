#!/bin/bash

APP=$HOME/.silt/
CONFIG=$APP/silt.ini
BINLOC=/usr/local/bin/silt

if [ "$(id -u)" != "0" ]; then
    echo "You must be root to install this script." 1>&2
    exit 1
else
    echo "This will install 'silt'"
    echo "[ENTER] to confirm"
    read confirm
    # I'm just going to package Requests with it instead. Using pip3 to install something is rude

    #check if app location exists; only make it if it exists
    if ! [ -e $APP ]; then
        mkdir -m 777 $APP
    fi

    echo "Getting/Unpacking requests..."
    wget -O /tmp/requests.tar.gz https://pypi.python.org/packages/source/r/requests/requests-2.8.1.tar.gz
    tar xvfz /tmp/requests.tar.gz -C $APP >/dev/null 2>&1
    cp /tmp/requests-2.8.1/requests $APP
    echo "Done."

    #cp will overwrite
    cp -p silt.py $APP/silt.py

    #if there's already something in the bin location, delete it
    if [ -e $BINLOC ]; then
        rm $BINLOC
    fi

    #make a softlink from the app location to the bin location
    ln -s $APP/silt.py $BINLOC

    if ! [ -e $CONFIG ]; then
        echo "Copying config..."
        cp -p silt.ini $CONFIG
    fi

    echo "Done. Enter 'silt' to run."
    echo "Config located at $HOME/.silt/silt.ini"
fi

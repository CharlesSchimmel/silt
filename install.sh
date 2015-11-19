#!/bin/bash
APP=$HOME/.silt/
CONFIG=$APP/silt.ini
BINLOC=/usr/local/bin/silt

if [[ "$(id -u)" != "0" ]]; then
    echo "You must be root to install this script." 1>&2
    exit 1
else
    # echo "This will install 'silt'"
    # echo "[[ENTER]] to confirm"
    # read confirm

    #check if app location exists; only make it if it exists
    if ! [[ -e $APP ]]; then
        mkdir -m 777 $APP
    fi

    echo "This will download dependencies 'requests' and 'pgi' from the python repository."
    echo "If you wish to install these yourself with Pip or you belive they are installed,"
    echo "enter 'n'"
    read confirm

    # Does what it says on the tin.
    # wget's files from the pypi repo to /tmp and untars them, then only grabs the needed folder
    if [[ $confirm != "n" ]]; then
        echo "Getting/Unpacking requests..."
        wget -O /tmp/requests.tar.gz https://pypi.python.org/packages/source/r/requests/requests-2.8.1.tar.gz >/dev/null 2>&1
        tar xvfz /tmp/requests.tar.gz >/dev/null 2>&1
        cp -r /tmp/requests-2.8.1/requests $APP >/dev/null 2>&1
        echo "Done."

        echo "Getting/Unpacking pgi..."
        wget -O /tmp/pgi.tar.gz https://pypi.python.org/packages/source/p/pgi/pgi-0.0.10.1.tar.gz >/dev/null 2>&1
        tar xvfz /tmp/pgi-0.0.10.1.tar.gz >/dev/null 2>&1
        cp -r /tmp/pgi-0.0.10.1/pgi $APP >/dev/null 2>&1
        echo "Done."
    else 
        echo "run 'pip3 install requests pgi' to install missing packages"
    fi 
    

    #cp will overwrite
    cp -p silt.py $APP/silt.py
    cp -p silt.desktop $HOME/.local/share/applications/silt.desktop

    #if there's already something in the bin location, delete it
    if [[ -e $BINLOC ]]; then
        rm $BINLOC
    fi

    #make a softlink from the app location to the bin location
    ln -s $APP/silt.py $BINLOC

    if ! [[ -e $CONFIG ]]; then
        echo "Copying config..."
        cp -p silt.ini $CONFIG
    fi

    echo "Please enter your username in the config located at $HOME/.silt/silt.ini, then enter silt to run. "
fi

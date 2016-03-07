#!/bin/bash
APP=$HOME/.silt/
CONFIG=$APP/silt.ini
BINLOC=/usr/local/bin/silt

if [[ "$(id -u)" != "0" ]]; then
    echo "You must be root to install this application." 1>&2
    exit 1
else
    echo "This will install 'silt'"
    echo -n "Checking dependencies..."

    #Check if python3 installed
    python3 --version >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Python3 is not installed. It is required for this application. Please install Python3 and retry installation."
        exit 1
    else
        echo -n "Python3 found..."
    fi

    # Check if pip3 installed
    pip3 --version >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Pip3 is not installed. It is required for this application. Please install Pip3 and retry installation."
        exit 1
    else
        echo -n "Pip3 found..."
    fi

    # Check if requests is installed
    sudo -H pip3 show requests >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then # Either pip3 isn't installed or requests isn't installed.
        # Requests not installed. Get requests. 
        echo -n "Requests not found, may I install it for you? [Y/n]"
        read response
        if [[ -z $response || $response == "Y" || $response == "y" ]]; then
            sudo -H pip3 install requests >/dev/null 2>&1
            if [[ $? -eq 0 ]]; then
                echo "Requests installed, proceeding."
            else
                echo "Unable to install requests, please consult your distro's documentation and install it before continuing."
                exit 1
            fi
        else
            echo "Unable to install requests, please consult your distro's documentation and install it before continuing."
            exit 1
        fi
    else
        echo -n "Requests found..."
    fi

    # Check if pgi is installed
    sudo -H pip3 show pgi >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then # Either pip3 isn't installed or pgi isn't installed.
        # pgi not installed. Get pgi. 
        echo -n "pgi not found, may I install it for you? [Y/n]"
        read response
        if [[ -z $response || $response == "Y" || $response == "y" ]]; then
            sudo -H pip3 install pgi >/dev/null 2>&1
            if [[ $? -eq 0 ]]; then
                echo "pgi installed, proceeding."
            else
                echo "Unable to install pgi, please install consult your distro's documentation and install it before continuing."
                exit 1
            fi
        else
            echo "Unable to install pgi, please install consult your distro's documentation and install it before continuing."
            exit 1
        fi
    else
        echo -n "Pgi found..."
    fi

    #check if app location exists; only make it if it exists
    if ! [[ -e $APP ]]; then
        mkdir -m 777 $APP
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

    echo "Please enter your username in the config located at $HOME/.silt/silt.ini, then use "silt" to run. "
fi

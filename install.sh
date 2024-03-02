#!/bin/bash

# remove previous version if present
./uninstall.sh

# copy project directory into kernel sources
cp -R . /usr/src/acer-wmi-battery-1.0

# register module in dkms and install
dkms add -m acer-wmi-battery -v 1.0
dkms build -m acer-wmi-battery -v 1.0
dkms install -m acer-wmi-battery -v 1.0

# auto-load module at boot
cp acer-wmi-battery.conf /etc/modules-load.d

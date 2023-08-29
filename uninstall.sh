#!/bin/bash

rm -rf /usr/src/acer-wmi-battery-1.0
dkms remove -m acer-wmi-battery -v 1.0
rm /etc/modules-load.d/acer-wmi-battery.conf

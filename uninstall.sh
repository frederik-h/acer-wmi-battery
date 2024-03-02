#!/bin/bash

dkms remove -m acer-wmi-battery/1.0 --all
rm -rf /usr/src/acer-wmi-battery-1.0
rm /etc/modules-load.d/acer-wmi-battery.conf

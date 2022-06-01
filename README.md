# acer-wmi-battery

## Description

This repository contains an experimental Linux kernel driver for the
battery health control WMI interface of Acer laptops.  It can be
used to enable/disable the battery health mode that can be enabled
through the "Acer Care Center" program on Windows.

So far, the driver has only been tested on an Acer Swift 3
(SF314-34). Any feedback on how it works on other Acer laptops
would be appreciated.

## Building

Make sure that you have the kernel headers for your kernel installed
and type `make` in the cloned project directory. In more detail,
on a Debian or Ubuntu system, you can build by:
```
sudo apt install build-essential linux-headers-$(uname -r)
git clone https://github.com/frederik-h/acer-wmi-battery.git
cd acer-wmi-battery
make
```

## Using

Loading the module without any parameters does not
change the health mode settings of your system:

```
insmod acer-wmi-battery.ko
```

The charge limit can then be enabled as follows:
```
echo 1 > /sys/bus/wmi/drivers/acer-wmi-battery/health_mode
```

Alternatively, you can enable it at module initialization
time:
```
insmod acer-wmi-battery.ko enable_health_mode=1
```





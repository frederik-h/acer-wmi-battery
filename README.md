# acer-wmi-battery

## Description

This repository contains an experimental Linux kernel driver for the
battery health control WMI interface of Acer laptops.  It can be used
to control two battery-related features of Acer laptops that Acer
provides through the Acer Care Center on Windows: a health mode that
limits the battery charge to 80% with the goal of preserving your
battery's capacity and a battery calibration mode which puts your
battery through a controlled charge-discharge cycle to provide more
accurate battery capacity estimates.

The driver has been developed on an Acer Swift 3
(SF314-34) laptop. Users have reported that it also works on other Acer laptops.
A list of those models can be found [here](MODELS.md).
Any feedback on how it works on Acer laptops not found on this list is appreciated.

## Building

Make sure that you have the kernel headers for your kernel installed
and type `make` in the cloned project directory. In more detail,
on a Debian or Ubuntu system, you can build by:
```
sudo apt install build-essential linux-headers-$(uname -r) git
git clone https://github.com/frederik-h/acer-wmi-battery.git
cd acer-wmi-battery
make
```

## Using

Loading the module without any parameters does not
change any health or calibration mode settings of your system:

```
sudo insmod acer-wmi-battery.ko
```

### Health mode

The charge limit can then be enabled as follows:
```
echo 1 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/health_mode
```

Alternatively, you can enable it at module initialization
time:
```
sudo insmod acer-wmi-battery.ko enable_health_mode=1
```

### Calibration mode

Before attempting the battery calibration, connect
your laptop to a power supply. The calibration mode
can be started as follows:
```
echo 1 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode
```


The calibration disables health mode and charges
to 100%. Then it discharges and recharges the battery
once. This can take a long time and for accurate
capacity estimates the laptop should not be used
during this process. After the discharge-charge cycle
the calibration mode should be manually disabled
since the WMI event that indicates the completion
of the calibration is not yet handled by the module:
```
echo 0 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode
```

### Related work

There exists [another driver](https://github.com/maxco2/acer-battery-wmi) with
similar functionality of which I have not been aware when starting the work
on this driver. See this [issue](https://github.com/frederik-h/acer-wmi-battery/issues/2) for discussion.

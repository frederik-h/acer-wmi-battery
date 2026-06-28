KERNELRELEASE ?= $(shell uname -r)
KDIR ?= /lib/modules/$(KERNELRELEASE)/build
MODDIR ?= /lib/modules/$(KERNELRELEASE)/extra

obj-m += acer-wmi-battery.o
PWD := $(CURDIR)

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

install: all
	install -D -m 0644 acer-wmi-battery.ko $(MODDIR)/acer-wmi-battery.ko
	depmod -a $(KERNELRELEASE)

uninstall:
	rm -f $(MODDIR)/acer-wmi-battery.ko
	depmod -a $(KERNELRELEASE)

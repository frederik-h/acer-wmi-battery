obj-m += acer-wmi-battery.o
PWD := $(CURDIR)
MDIR := /lib/modules/$(shell uname -r)/kernel/drivers/platform/x86
MODNAME := acer-wmi-battery

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

install: all
	sudo install -d $(MDIR)
	sudo install -m 644 $(MODNAME).ko $(MDIR)
	sudo depmod -a
	@echo "$(MODNAME)" | sudo tee /etc/modules-load.d/$(MODNAME).conf > /dev/null
	sudo modprobe $(MODNAME)
	@echo "Installed $(MODNAME) and will load at boot."

uninstall:
	sudo rm -f /etc/modules-load.d/$(MODNAME).conf
	sudo modprobe -r $(MODNAME)
	sudo rm -f $(MDIR)/$(MODNAME).ko
	sudo depmod -a
	@echo "Uninstalled $(MODNAME) and removed related configuration."

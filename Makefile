obj-m += acer-wmi-battery.o
PWD := $(CURDIR)

all:
	make -C /lib/modules/$(KERNELVERSION)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(KERNELVERSION)/build M=$(PWD) clean

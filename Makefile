obj-m += acer-wmi-battery.o
PWD := $(CURDIR)
KVERSION ?= $(shell uname -r)
KDIR ?= /lib/modules/$(KVERSION)/build

all:
	make -C $(KDIR) M=$(PWD) modules

clean:
	make -C $(KDIR) M=$(PWD) clean

obj-m += acer-wmi-battery.o
PWD := $(CURDIR)

# Kernel to build against (override with: make KVER=<version>)
KVER ?= $(shell uname -r)
KBUILD := /lib/modules/$(KVER)/build

# Kernels compiled with clang and ThinLTO (e.g. the default CachyOS kernel)
# require external modules to be built with the LLVM toolchain as well.
# Detect the compiler the kernel was built with and enable LLVM=1 if needed.
ifeq ($(shell grep -c '^CONFIG_CC_IS_CLANG=y' $(KBUILD)/.config),1)
TOOLCHAIN := LLVM=1
endif

all:
	$(MAKE) -C $(KBUILD) M=$(PWD) $(TOOLCHAIN) modules

clean:
	$(MAKE) -C $(KBUILD) M=$(PWD) $(TOOLCHAIN) clean

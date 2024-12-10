obj-m += acer-wmi-battery.o
PWD := $(CURDIR)

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
# install:
# 	install -Dm755 gui.py $(DESTDIR)/usr/bin/acer-battery-control-gui
# 	install -Dm755 backend.py ${DESTDIR}/etc/acer-battery-control-gui/backend.py
#   	install -Dm755 acer-battery-control-gui.service ${DESTDIR}/usr/lib/systemd/system/acer-battery-control-gui.service
# 	install -Dm755 acer-wmi-battery.c $(DESTDIR)/etc/acer-battery-control-gui/acer-wmi-battery.c
# 	install -Dm755 Makefile $(DESTDIR)/etc/acer-battery-control-gui/Makefile
# 	install -Dm644 acer-battery-health.desktop $(DESTDIR)/usr/share/applications/acer-battery-health.desktop
# 	install -Dm644 acer-care-center_48x48.png $(DESTDIR)/usr/share/icons/hicolor/48x48/apps/acer-battery-control.png #  Adjust icon path as needed
# 	install -Dm644 acer-care-center_256x256.png $(DESTDIR)/usr/share/icons/hicolor/256x256/apps/acer-battery-control.png #  Adjust icon path as needed
#     #  install other files like acer-wmi-battery.ko if necessary
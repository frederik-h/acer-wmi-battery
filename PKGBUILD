pkgname=acer-battery-control-gui
pkgver=1.1.0
pkgrel=2
pkgdesc="A simple GUI to control Acer battery health mode."
arch=("any")
url="Your project URL"
license=("MIT")  # Thay đổi theo license của bạn
depends=("python3" "python-pyqt5")
makedepends=("python") #  Only needed if you're building anything during the package creation
provides=("acer-battery-manager") #  Optional: other names this package provides
conflicts=("acer-battery-manager-other") # Optional: packages that conflict with this one

source=(
    "gui.py"
    "backend.py"
    "acer-battery-control-gui.service"
    "acer-battery-control.rules"
    "acer-wmi-battery.c"
    "Makefile"
    "acer-battery-health.desktop"
    "acer-care-center_48x48.png"  # Add 48x48 icon
    "acer-care-center_256x256.png" # Add 256x256 icon
    "LICENSE"
    "README.md"
)


md5sums=('64277873980bb22f74d5c7a9aa1a9f82'
         '195e4d652f464ea2a7d2df8bd09daa24'
         'f96c4057cf13978318760a4a882af1e6'
         '04f9aa5b03321da2fa1937392cfb9020'
         'fbc8ba053c24c6632f94d9484147d118'
         '792e8072c180a203ace0c478ce9f1798'
         '377c5f4ef1218dec09967bfea74fa3b2'
         '271fb148077017e87d114f000c9f5ce4'
         '268602bfba61e6ee16de750be4a0469b'
         'b234ee4d69f5fce4486a80fdaf4a4263'
         '8009a8fc6b9a93f5df053478df2aeb07')

package() {
  install -Dm755 gui.py "${pkgdir}/usr/bin/acer-battery-control-gui"
  install -Dm755 backend.py "${pkgdir}/etc/acer-battery-control-gui/backend.py"
  install -Dm644 acer-battery-control.rules "${pkgdir}/usr/share/polkit-1/rules.d/acer-battery-control.rules"
  install -Dm755 acer-battery-control-gui.service "${pkgdir}/usr/lib/systemd/system/acer-battery-control-gui.service"
  install -Dm755 acer-wmi-battery.c "${pkgdir}/etc/acer-battery-control-gui/acer-wmi-battery.c"
  install -Dm755 Makefile "${pkgdir}/etc/acer-battery-control-gui/Makefile"
  install -Dm644 acer-battery-health.desktop "${pkgdir}/usr/share/applications/acer-battery-health.desktop"
  install -Dm644 acer-care-center_256x256.png "${pkgdir}/usr/share/icons/hicolor/256x256/apps/acer-battery-control.png"
  install -Dm644 acer-care-center_48x48.png "${pkgdir}/usr/share/icons/hicolor/48x48/apps/acer-battery-control.png"
  # Install other files
  post_install() {
    ln -s /usr/lib/systemd/system/acer-battery-control-gui.service /etc/systemd/system/
    systemctl enable acer-battery-control-gui.service
    systemctl restart acer-battery-control-gui.service
    systemctl restart polkit
  }
}

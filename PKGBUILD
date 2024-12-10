pkgname=acer-battery-control-gui
pkgver=1.0.0
pkgrel=3
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
    "acer-wmi-battery.c"
    "Makefile"
    "acer-battery-health.desktop"
    "acer-care-center_48x48.png"  # Add 48x48 icon
    "acer-care-center_256x256.png" # Add 256x256 icon
    "LICENSE"
    "README.md"
)


md5sums=('405eecd7f6617315cec74748ddff9b0f'
         'fbc8ba053c24c6632f94d9484147d118'
         'bd8723ba7cc3d9c40a5ff1dedbda23bc'
         '377c5f4ef1218dec09967bfea74fa3b2'
         '271fb148077017e87d114f000c9f5ce4'
         '268602bfba61e6ee16de750be4a0469b'
         'b234ee4d69f5fce4486a80fdaf4a4263'
         '8009a8fc6b9a93f5df053478df2aeb07')

package() {
  install -Dm755 gui.py "${pkgdir}/usr/bin/acer-battery-control-gui"
  install -Dm755 acer-wmi-battery.c "${pkgdir}/etc/acer-battery-control-gui/acer-wmi-battery.c"
  install -Dm755 Makefile "${pkgdir}/etc/acer-battery-control-gui/Makefile"
  install -Dm644 acer-battery-health.desktop "${pkgdir}/usr/share/applications/acer-battery-health.desktop"
  install -Dm644 acer-care-center_256x256.png "${pkgdir}/usr/share/icons/hicolor/256x256/apps/acer-battery-control.png"
  install -Dm644 acer-care-center_48x48.png "${pkgdir}/usr/share/icons/hicolor/48x48/apps/acer-battery-control.png"
  # Install other files
}

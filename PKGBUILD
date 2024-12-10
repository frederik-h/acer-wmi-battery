pkgname=acer-battery-control-gui
pkgver=1.0.0
pkgrel=1
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
    "acer-battery-health.desktop"
    "acer-care-center_48x48.png"  # Add 48x48 icon
    "acer-care-center_256x256.png" # Add 256x256 icon
    "LICENSE"
    "README.md"
)


md5sums=('fb00743481f5bf8e5735c20eac9370e1'
         '377c5f4ef1218dec09967bfea74fa3b2'
         '271fb148077017e87d114f000c9f5ce4'
         '268602bfba61e6ee16de750be4a0469b'
         'b234ee4d69f5fce4486a80fdaf4a4263'
         'e1bfd5e2f773bbf2bbadae373d502cf8')

package() {
  install -Dm755 gui.py "${pkgdir}/usr/bin/acer-battery-control-gui"
  install -Dm644 acer-battery-health.desktop "${pkgdir}/usr/share/applications/acer-battery-health.desktop"
  install -Dm644 acer-care-center_256x256.png "${pkgdir}/usr/share/icons/hicolor/256x256/apps/acer-battery-control.png"
  install -Dm644 acer-care-center_48x48.png "${pkgdir}/usr/share/icons/hicolor/48x48/apps/acer-battery-control.png"
  # Install other files
}

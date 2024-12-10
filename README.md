# acer-wmi-battery

## Mô tả

Repository này chứa một driver kernel Linux thử nghiệm cho giao diện WMI điều khiển tình trạng pin của máy tính xách tay Acer. Nó có thể được sử dụng để điều khiển hai tính năng liên quan đến pin mà Acer cung cấp thông qua Acer Care Center trên Windows: chế độ bảo vệ pin (giới hạn sạc pin ở mức 80% nhằm bảo vệ dung lượng pin) và chế độ hiệu chỉnh pin (thực hiện chu kỳ sạc-xả có kiểm soát để cung cấp ước tính dung lượng pin chính xác hơn).

Các thiết bị hoạt động
- Acer Swift 3 SF314-34
- Acer Aspire 5 A515-45G-R5A1
- Acer Enduro N3 Urban EUN314A-51W
- Acer Nitro 5 AN515-45 (của tôi) (OS: Manjaro, kernel: linux 6.10.13-3 )

## Cài đặt

Driver này có thể được cài đặt từ AUR:
```bash
yay -U acer-wmi-battery-gui{version}.pkg.tar.zst
```

## Sử dụng

### Chế độ bảo vệ pin

Chế độ này giới hạn sạc pin ở mức 80% để kéo dài tuổi thọ pin.  Bạn có thể bật/tắt chế độ này trong ứng dụng GUI.

### Chế độ hiệu chỉnh pin

Chế độ này thực hiện chu kỳ sạc-xả pin để hiệu chỉnh lại dung lượng pin.

**Lưu ý:**

* Trước khi bắt đầu hiệu chỉnh pin, hãy kết nối máy tính xách tay với nguồn điện.
* Quá trình hiệu chỉnh có thể mất nhiều thời gian.  Để có kết quả chính xác, không nên sử dụng máy tính trong quá trình này.
* Sau khi hoàn thành chu kỳ xả-sạc, bạn nên tắt chế độ hiệu chỉnh pin bằng tay.


## Xây dựng từ nguồn

Nếu bạn muốn tự build driver từ nguồn, hãy chắc chắn rằng bạn đã cài đặt kernel headers và chạy lệnh `make` trong thư mục project:

```bash
sudo apt install build-essential linux-headers-$(uname -r) git
git clone https://github.com/frederik-h/acer-wmi-battery.git
cd acer-wmi-battery
make
```

Sau đó, bạn có thể nạp module bằng lệnh:

```bash
sudo insmod acer-wmi-battery.ko
```


## Dự án liên quan

Một driver khác có chức năng tương tự: [acer-battery-wmi](https://github.com/maxco2/acer-battery-wmi).
```

README này sẽ giúp người dùng hiểu rõ hơn về dự án và cách sử dụng.  Nó cũng cung cấp hướng dẫn cài đặt đơn giản từ AUR, giúp người dùng dễ dàng cài đặt và sử dụng driver.

# My ADB Lib

Thư viện Python wrapper cho Android Debug Bridge (ADB) không yêu cầu phụ thuộc bên ngoài.

## Giới thiệu

My ADB Lib là một thư viện Python giúp tương tác với thiết bị Android thông qua ADB (Android Debug Bridge). Thư viện này được thiết kế để đơn giản hóa việc sử dụng các lệnh ADB trong các ứng dụng Python, tự động hóa kiểm thử, và quản lý thiết bị Android.

## Yêu cầu

- Python 3.6 trở lên
- ADB đã được cài đặt và có trong PATH

## Cài đặt

```bash
pip install my-adb-lib
```

Hoặc cài đặt từ mã nguồn:

```bash
git clone https://github.com/yourusername/my-adb-lib.git
cd my-adb-lib
pip install -e .
```

## Cách sử dụng

### Khởi tạo

```python
from my_adb_lib import MyADB

# Khởi tạo với thiết bị mặc định
adb = MyADB()

# Hoặc chỉ định thiết bị cụ thể
adb = MyADB(device_id="emulator-5554")
```

### Các thao tác cơ bản

```python
# Liệt kê các thiết bị đã kết nối
devices = adb.get_devices()
print(devices)

# Cài đặt ứng dụng
adb.install_app("/path/to/app.apk")

# Gỡ cài đặt ứng dụng
adb.uninstall_app("com.example.app")

# Khởi động lại thiết bị
adb.reboot_device()
```

### Tương tác với thiết bị

```python
from my_adb_lib.commands import interaction

# Nhấn vào tọa độ màn hình
interaction.tap(500, 500)

# Vuốt màn hình
interaction.swipe(100, 500, 600, 500)

# Nhập văn bản
interaction.text_input("Hello World")

# Nhấn phím Home
interaction.home()
```

### Quản lý file

```python
from my_adb_lib.commands import file_ops

# Đẩy file từ máy tính lên thiết bị
file_ops.push("/path/on/computer", "/path/on/device")

# Lấy file từ thiết bị về máy tính
file_ops.pull("/path/on/device", "/path/on/computer")
```

### Xem log

```python
from my_adb_lib.commands import logs

# Xem logcat
logcat_output = logs.logcat()
print(logcat_output)

# Tạo báo cáo lỗi
bugreport = logs.bugreport()
```

## Tài liệu API

### Lớp MyADB

Lớp chính để tương tác với ADB.

- `__init__(device_id=None)`: Khởi tạo đối tượng ADB với ID thiết bị tùy chọn
- `run(command)`: Chạy lệnh ADB tùy chỉnh
- `get_devices()`: Liệt kê các thiết bị đã kết nối
- `reboot_device()`: Khởi động lại thiết bị
- `install_app(apk_path)`: Cài đặt ứng dụng từ file APK
- `uninstall_app(package_name)`: Gỡ cài đặt ứng dụng
- `push_file(local_path, remote_path)`: Đẩy file lên thiết bị
- `pull_file(remote_path, local_path)`: Lấy file từ thiết bị
- `get_device_info()`: Lấy thông tin thiết bị

### Module commands

Các module lệnh chuyên biệt:

- `app_info`: Lấy thông tin ứng dụng
- `apps`: Quản lý ứng dụng
- `basic`: Các lệnh ADB cơ bản
- `connect`: Kết nối thiết bị qua mạng
- `device_actions`: Các hành động thiết bị
- `device_info`: Thông tin thiết bị
- `file_ops`: Thao tác file
- `interaction`: Tương tác với thiết bị
- `logs`: Xem log thiết bị
- `permissions`: Quản lý quyền

## Đóng góp

Đóng góp luôn được chào đón! Vui lòng tạo issue hoặc pull request trên GitHub.

## Giấy phép

MIT License

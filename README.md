# Cấu trúc dự án

**`app/`**
- `auth.py` - Chứa các chức năng làm việc trên Flask-Login, như hàm `load_user`
- `dao.py` - Chứa logic truy cập dữ liệu
- `models.py` (Chứa các mô hình dữ liệu như `User`)
- `database.py` (Quản lý kết nối cơ sở dữ liệu)
- `utils.py` - Chứa các tiện ích chung, không phụ thuộc vào một module cụ thể nào

**`models/`**
- `__init__.py` - Định nghĩa các model
- `__main__.py` - Phục vụ cho việc khởi tạo Model thành các bảng trong cơ sở dữ liệu
- `seed/` - Chứa các dữ liệu ảo được dùng để test chương trình

**Cấu trúc id của Lớp học**
```
Năm học kỳ (2 con số) + Khối lớp + Số lớp (A, B, C, E)
```
Ví dụ lớp 12B năm học 2022 - 2023: `2212A`
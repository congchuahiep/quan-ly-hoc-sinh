from app import app, db

from models import NguoiDung, NhanVien, GiaoVien, QuanTri, LopHoc, DayLop, MonHoc, HocSinh, HocKy, HocSinhLop

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
from app import app, db

from models.user import NguoiDung, NhanVien, GiaoVien, QuanTri
from models.classroom import LopHoc, DayLop
from models.student import HocSinh, HocSinhLop
from models.course import MonHoc, HocKy, BangDiem, Diem15Phut, DiemMotTiet

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
from datetime import date
import random
from app import db


def get_khoi_lop(khoi_lop):
    return "Khoi" + str(khoi_lop)
    

# Hàm thêm các học sinh vào vào lớp
def xep_lop(lop_hoc, hoc_sinhs, ngay_bat_dau=date.today()):
    from models import HocSinhLop

    # Thêm học sinh vào lớp
    for hoc_sinh in hoc_sinhs:
        hoc_sinh_lop = HocSinhLop(
            hoc_sinh_id=hoc_sinh.id,
            lop_hoc_id=lop_hoc.id,
            ngay_bat_dau=ngay_bat_dau,  # Ngày bắt đầu học
            trang_thai="DangHoc"
        )
        db.session.add(hoc_sinh_lop)


from datetime import date
import random

from sqlalchemy import exists, extract
from app import db
from app.utils import chia_cac_phan_ngau_nhien, get_nam_sinh
    

# Hàm thêm các học sinh vào vào lớp
def them_cac_hoc_sinh_vao_lop(lop_hoc, hoc_sinhs, ngay_bat_dau=date.today()):
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
        
        
def tao_lop():
    return None


def xep_lop(nam_hoc, khoi_lop=10):
    from models import HocSinh, LopHoc, KhoiLop, HocKy
    
    # Truy vấn các học sinh và các lớp
    full_hoc_sinhs = HocSinh.query.filter(extract('year', HocSinh.ngay_sinh) == get_nam_sinh(nam_hoc, khoi_lop)).all()
    lop_hocs = LopHoc.query.filter(LopHoc.hai_hoc_ky.any(HocKy.nam_hoc == nam_hoc), LopHoc.khoi_lop == KhoiLop(khoi_lop)).all()
    
    if (len(lop_hocs) == 0):
        lop_hocs = tao_lop()
        
        print("Không có lớp?", lop_hocs)
        
        return
    
    so_luong_lop = len(lop_hocs)
    
    # Cắt danh sách học sinh thành các phần
    si_so_tung_lop = chia_cac_phan_ngau_nhien(len(full_hoc_sinhs), so_luong_lop, 33, 40)
    index = 0
    
    for i in range(so_luong_lop):
        them_cac_hoc_sinh_vao_lop(lop_hoc=lop_hocs[i], hoc_sinhs=full_hoc_sinhs[index:index + si_so_tung_lop[i]])
        index += si_so_tung_lop[i]
        
def giao_vien_khong_chu_nhiem(nam_hoc):
    from models import LopHoc, GiaoVien
    
    return GiaoVien.query.filter(
            ~GiaoVien.lop_chu_nhiem.has(LopHoc.nam_hoc == nam_hoc)
        ).all()
    
def tao_khoi_10_moi(nam_hoc, so_luong=5):
    from models import LopHoc, KhoiLop
    
    cac_giao_vien_chu_nhiem = giao_vien_khong_chu_nhiem(nam_hoc-1)
    
    for i in range(so_luong):
        ten_lop = "10" + chr(65 + i)
        
        lop_hoc = LopHoc(
            id=str(nam_hoc) + ten_lop,
            ten_lop=ten_lop,
            nam_hoc=nam_hoc,
            khoi_lop=KhoiLop(10),
            giao_vien_chu_nhiem_id=cac_giao_vien_chu_nhiem[i].id
        )
        
        db.session.add(lop_hoc)
    db.session.commit()

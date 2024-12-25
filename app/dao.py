from datetime import date
import random

from sqlalchemy import exists, extract
from app import db
from app.utils import chia_cac_phan_ngau_nhien, get_hoc_ky, get_nam_sinh
    

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

def phan_cong_ngau_nhien_giao_vien_day_hoc(nam_hoc):
    from models import LopHoc, GiaoVien, MonHoc, DayLop
    
    so_mon_hoc = MonHoc.query.count()
    lop_hocs = LopHoc.query.filter(LopHoc.nam_hoc == nam_hoc).all()
    
    (hoc_ky_mot, hoc_ky_hai) = get_hoc_ky(nam_hoc)

    #1. Phân công giáo viên chủ nhiệm
    for i in range(len(lop_hocs)):
        lop = lop_hocs[i]
        giao_vien_chu_nhiem = GiaoVien.query.get(lop.giao_vien_chu_nhiem_id)
        
        # Chọn môn học ngẫu nhiên mà giáo viên chủ nhiệm dạy
        mon_hoc = random.choice(giao_vien_chu_nhiem.day_mon)
        
        day_lop_ky_mot = DayLop(
            lop_hoc_id = lop.id,
            giao_vien_id = lop.giao_vien_chu_nhiem_id,
            mon_hoc_id = mon_hoc.id,
            hoc_ky_id = hoc_ky_mot
        )
        
        day_lop_ky_hai = DayLop(
            lop_hoc_id = lop.id,
            giao_vien_id = lop.giao_vien_chu_nhiem_id,
            mon_hoc_id = mon_hoc.id,
            hoc_ky_id = hoc_ky_hai
        )
        
        db.session.add_all([day_lop_ky_mot, day_lop_ky_hai])
        db.session.commit()
        
    #2. Phân công thêm các giáo viên và môn học còn lại
    for lop in lop_hocs:
        # Lấy danh sách các giáo viên trừ giáo viên đã dạy
        giao_vien_da_phan_cong_id = {gv.id for gv in lop.giao_vien_day_lop}
        # Lấy danh sách các môn học đã có
        mon_hoc_da_co_id = {gv_lh.mon_hoc_id for gv_lh in lop.giao_vien_day_lop}
        
        while len(mon_hoc_da_co_id) < so_mon_hoc:
            # Lọc môn học còn thiếu
            mon_hoc_con_thieu = MonHoc.query.filter(~MonHoc.id.in_(mon_hoc_da_co_id)).first()
            
            # Lọc danh sách các giáo viên dạy môn học còn thiếu
            giao_viens = GiaoVien.query.filter(GiaoVien.day_mon.any(MonHoc.id == mon_hoc_con_thieu.id)).all()
            # Lọc danh sách các giáo viên đã dạy lớp này
            giao_viens = GiaoVien.query.filter(~GiaoVien.id.in_(giao_vien_da_phan_cong_id)).all()
            giao_vien = random.choice(giao_viens)
            
            day_lop_ky_mot = DayLop(
                lop_hoc_id = lop.id,
                giao_vien_id = giao_vien.id,
                mon_hoc_id = mon_hoc_con_thieu.id,
                hoc_ky_id = hoc_ky_mot
            )
            
            day_lop_ky_hai = DayLop(
                lop_hoc_id = lop.id,
                giao_vien_id = giao_vien.id,
                mon_hoc_id = mon_hoc_con_thieu.id,
                hoc_ky_id = hoc_ky_hai
            )
            
            db.session.add_all([day_lop_ky_mot, day_lop_ky_hai])
            
            giao_vien_da_phan_cong_id.add(giao_vien.id)
            mon_hoc_da_co_id.add(mon_hoc_con_thieu.id)
        db.session.commit()
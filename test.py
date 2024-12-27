from sqlalchemy import extract
from app.utils import get_nam_sinh
from models import GiaoVien, HocKy, HocSinh, KhoiLop, LopHoc, BangDiem
from app import app, db

with app.app_context():
    # giao_vien = GiaoVien.query.get(1)
    
    # print(giao_vien)

    # lop_day = giao_vien.get_lop_giao_vien_day(241)
    # print(lop_day)
    # lop_hoc = lop_day[0]
    # print(lop_hoc)
    # bang_diem = lop_hoc.get_danh_sach_diem(mon_hoc_id=1, hoc_ky_id=241)
    # print(bang_diem)
    
    # TODO: Thêm học sinh 2k10 và xoá học sinh 2k4 cũng như năm học 21

    # hs = HocSinh.query.filter(extract('year', HocSinh.ngay_sinh) == get_nam_sinh(22, 10)).all()
    # lp = LopHoc.query.filter(LopHoc.hai_hoc_ky.any(HocKy.nam_hoc == 21), LopHoc.khoi_lop == KhoiLop(10)).all()
    # hk = HocKy.query.all()
    
    # print(hs)
    # print(lp)
    # print([h.nam_hoc for h in hk])
    
    
    mon_hoc_id = 1
    hoc_ky_id = 241
    khoi_lop = 10
    
    lop_hocs = LopHoc.query.filter(
        LopHoc.hai_hoc_ky.any(HocKy.id == hoc_ky_id),
        LopHoc.khoi_lop == KhoiLop(khoi_lop))
    
    danh_sach_tong_ket = []
    
    for lop_hoc in lop_hocs:
        tong_dat = lop_hoc.tinh_tong_dat_mon_hoc(mon_hoc_id, hoc_ky_id)
        ty_le_dat = lop_hoc.ty_le_dat_mon_hoc(tong_dat)
        
        tong_ket = {
            "ten_lop": lop_hoc.ten_lop,
            "tong_dat": tong_dat,
            "ty_le_dat": ty_le_dat
        }
        danh_sach_tong_ket.append(tong_ket)
    
    print(danh_sach_tong_ket)
    
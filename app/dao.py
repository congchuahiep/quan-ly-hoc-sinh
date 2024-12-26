from datetime import date
import random

from sqlalchemy import exists, extract
from app import db
from app.utils import chia_cac_phan_ngau_nhien, get_hoc_ky, get_nam_sinh
        
def tao_bang_diem_cho_lop(lop_hoc, mon_hoc, hoc_ky):
    from models import BangDiem
    
    hoc_sinhs = lop_hoc.get_danh_sach_hoc_sinh()
    
    for hoc_sinh in hoc_sinhs:
        bang_diem = BangDiem(
            hoc_sinh_id = hoc_sinh.id,
            mon_hoc_id = mon_hoc.id,
            hoc_ky_id = hoc_ky.id
        )
        db.session.add(bang_diem)
    db.session.commit()
        
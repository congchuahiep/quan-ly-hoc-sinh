from datetime import date
import json
import hashlib
import os

from sqlalchemy import extract

from app import app, db
from app.dao import get_khoi_lop, xep_lop
from app.utils import chia_cac_phan_ngau_nhien, get_nam_sinh
from models import HocSinh, LopHoc, MonHoc, GiaoVien, QuanTri, HocKy

# Lấy đường dẫn của thư mục hiện tại
script_dir = os.path.dirname(__file__)

def tao_giao_vien():
    giao_vien_path = os.path.join(script_dir, 'giaovien.json')
    
    with open(giao_vien_path, 'r', encoding= 'utf-8') as file:
        data = json.load(file)
        for item in data:
            giao_vien = GiaoVien(
                username=item['username'],
                password=item['password'],
                avatar=item['avatar'],
                ten=item['ten'],
                ho=item['ho'],
                ngay_sinh=item['ngay_sinh'],
                email=item['email'],
                dien_thoai=item['dien_thoai'],
                dia_chi=item['dia_chi'],
                loai_nguoi_dung=item['loai_nguoi_dung'],
                gioi_tinh=item['gioi_tinh']
            )
            db.session.add(giao_vien)
        db.session.commit()
        
        
def tao_mon_hoc():
    mon_hoc_path = os.path.join(script_dir, 'monhoc.json')
    
    with open(mon_hoc_path, 'r', encoding= 'utf-8') as file:
        data = json.load(file)
        for item in data:
            mon_hoc = MonHoc(
                ten_mon_hoc=item['ten_mon_hoc']
            )
            db.session.add(mon_hoc)
        db.session.commit()


def tao_quan_tri():
    quan_tri_path = os.path.join(script_dir, 'quantri.json')
    
    with open(quan_tri_path, 'r', encoding= 'utf-8') as file:
        data = json.load(file)
        for item in data:
            quan_tri = QuanTri(
                username=item['username'],
                password=item['password'],
                avatar=item['avatar'],
                ten=item['ten'],
                ho=item['ho'],
                ngay_sinh=item['ngay_sinh'],
                email=item['email'],
                dien_thoai=item['dien_thoai'],
                dia_chi=item['dia_chi'],
                loai_nguoi_dung=item['loai_nguoi_dung'],
                gioi_tinh=item['gioi_tinh']
            )
            db.session.add(quan_tri)
        db.session.commit()
            
            
def tao_hoc_sinh():
    hoc_sinh_file_paths = [
        "hocsinh2004.json",
        "hocsinh2005.json",
        "hocsinh2006.json",
        "hocsinh2007.json",
        "hocsinh2008.json",
        "hocsinh2009.json"
    ]
    
    for hoc_sinh_file_path in hoc_sinh_file_paths:
        hoc_sinh_path = os.path.join(script_dir, hoc_sinh_file_path)
        
        with open(hoc_sinh_path, 'r', encoding= 'utf-8') as file:
            data = json.load(file)
            for item in data:
                hoc_sinh = HocSinh(
                    ten=item['ten'],
                    ho=item['ho'],
                    ngay_sinh=item['ngay_sinh'],
                    email=item['email'],
                    dien_thoai=item['dien_thoai'],
                    dia_chi=item['dia_chi'],
                    gioi_tinh=item['gioi_tinh']
                )
                db.session.add(hoc_sinh)
            db.session.commit()
        

def tao_hoc_ky():
    hoc_ky_path = os.path.join(script_dir, 'hocky.json')
    
    with open(hoc_ky_path, 'r', encoding= 'utf-8') as file:
        data = json.load(file)
        for item in data:
            hoc_ky = HocKy(
                id=item['id']
            )
            db.session.add(hoc_ky)
        db.session.commit()
        
        
def tao_lop_hoc():
    lop_hoc_path = os.path.join(script_dir, 'lophoc.json')
    
    with open(lop_hoc_path, 'r', encoding= 'utf-8') as file:
        data = json.load(file)
        
        giao_vien_chu_nhiem_count = 0
        
        for i in range(4):
            namHoc = 21 + i
            
            for item in data:
                
                lop_hoc = LopHoc(
                    id=str(namHoc) + item['ten_lop'],
                    ten_lop=item['ten_lop'],
                    khoi_lop=item['khoi_lop'],
                    giao_vien_chu_nhiem_id=giao_vien_chu_nhiem_count % 20 + 1
                )
                
                lop_hoc.hai_hoc_ky.extend(HocKy.query.filter(HocKy.id > 210 + i * 10, HocKy.id < 220 + i * 10).all())
                db.session.add(lop_hoc)
                giao_vien_chu_nhiem_count += 1
        db.session.commit()
                
                
                
def tao_hoc_sinh_lop():
    
    # Lặp qua các năm học != học kỳ
    hocKy = 211
    
    # Lặp qua các khối lớp
    for khoi_lop in [10, 11, 12]:
        xep_lop(hocKy, khoi_lop)
            
    


if __name__ == '__main__':
    
    with app.app_context():
        print('Tạo dữ liệu mẫu...')
        
        db.create_all()
                     
        # Tạo dữ liệu mẫu
        # tao_giao_vien()
        # tao_mon_hoc()
        # tao_quan_tri()
        # tao_hoc_sinh()
        # tao_hoc_ky()
        # tao_lop_hoc()
        
        tao_hoc_sinh_lop()
        
                    
        db.session.commit()
        print('Tạo dữ liệu mẫu thành công')
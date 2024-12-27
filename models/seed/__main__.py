from datetime import date
import json
import hashlib
import os
import random

from sqlalchemy import extract

from app import app, db

from app.utils import get_hoc_ky
from models import GiaoVien, HocSinh, QuanTri, HocKy, MonHoc, LopHoc, KhoiLop, BangDiem
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
        
        
def tao_lop_hoc_nam_21():
    lop_hoc_path = os.path.join(script_dir, 'lophoc.json')
    
    with open(lop_hoc_path, 'r', encoding= 'utf-8') as file:
        data = json.load(file)
        
        giao_vien_chu_nhiem_count = 0
        
        # Ta chỉ tạo riêng các lớp học trong năm 21, phần tạo các lớp trong kỳ khác sẽ được triển
        # khai vào #TODO
        namHoc = 21
        
        for item in data:
            
            lop_hoc = LopHoc(
                id=str(namHoc) + item['ten_lop'],
                nam_hoc=21,
                ten_lop=item['ten_lop'],
                khoi_lop=KhoiLop(item['khoi_lop']),
                giao_vien_chu_nhiem_id=giao_vien_chu_nhiem_count % 20 + 1
            )
            lop_hoc.hai_hoc_ky.extend(HocKy.query.filter(HocKy.id > 210, HocKy.id < 220).all())
            db.session.add(lop_hoc)
            giao_vien_chu_nhiem_count += 1
        db.session.commit()
                
                
def tao_hoc_sinh_lop_nam_21():
    # Lặp qua các năm học != học kỳ
    nam_hoc = 21
    
    # Lặp qua các khối lớp
    for khoi_lop in [10, 11, 12]:
        LopHoc.xep_lop(nam_hoc, khoi_lop)
            
            
def tao_lop_hoc_va_hoc_sinh_lop_con_lai():
    for nam_hoc_moi in [22, 23, 24]:
        nam_hoc_cu = nam_hoc_moi - 1
        lop_hocs = LopHoc.query.filter(LopHoc.nam_hoc == nam_hoc_cu).all()
        
        print(lop_hocs)
        
        for lop_hoc in lop_hocs:
            lop_hoc.len_lop()
            
        # Tạo lớp 10 mới
        LopHoc.tao_khoi_10_moi(nam_hoc_moi)
        
        # Xếp các học sinh năm mới vào lớp
        LopHoc.xep_lop(nam_hoc_moi)
            
def phan_mon_giao_vien():
    day_mon_path = os.path.join(script_dir, 'daymon.json')
    
    with open(day_mon_path, 'r', encoding= 'utf-8') as file:
        data = json.load(file)
        for item in data:
            mon_hoc = MonHoc.query.get(item['mon_hoc_id'])
            giao_vien = GiaoVien.query.get(item['giao_vien_id'])
            
            giao_vien.day_mon.append(mon_hoc)
        db.session.commit()
        

def phan_lop_giao_vien():
    for nam_hoc in [21, 22, 23, 24]:
    
        lop_hocs = LopHoc.query.filter(LopHoc.nam_hoc == nam_hoc).all()
        
        for lop_hoc in lop_hocs:
            lop_hoc.phan_cong_ngau_nhien_giao_vien_day_hoc()
            
def tao_bang_diem():
    mon_hocs = MonHoc.query.all()
    
    for nam_hoc in [21, 22, 23, 24]:
        lop_hocs = LopHoc.query.filter(LopHoc.nam_hoc == nam_hoc).all()
        for lop_hoc in lop_hocs:
            (hoc_ky_mot, hoc_ky_hai) = get_hoc_ky(nam_hoc)
            
            for mon_hoc in mon_hocs:
                lop_hoc.tao_bang_diem_cho_lop(mon_hoc, hoc_ky_mot)
            
            if nam_hoc != 24:
                for mon_hoc in mon_hocs:
                    lop_hoc.tao_bang_diem_cho_lop(mon_hoc, hoc_ky_hai)
                    
        print("Đã tạo xong bảng điểm năm học: ", nam_hoc)
        
def cap_nhat_diem():
    bang_diems = BangDiem.query.all()
    
    # Tạo danh sách các giá trị của điểm là hệ số của là 0.25
    diems = [i * 0.25 for i in range(0, 41)]
    
    for bang_diem in bang_diems:
        diem_15_phut = random.choice(diems)
        diem_mot_tiet = random.choice(diems)
        diem_cuoi_ky = random.choice(diems)
        
        bang_diem.update_diem_15_phut(diem_15_phut)
        bang_diem.update_diem_mot_tiet(diem_mot_tiet)
        bang_diem.update_diem_cuoi_ky(diem_cuoi_ky)

if __name__ == '__main__':
    
    with app.app_context():
        print('Tạo dữ liệu mẫu...')
        
        db.create_all()
                     
        ## Tạo dữ liệu basic
        print("Khởi tạo dữ liệu căn bản cho hệ thống")
        tao_giao_vien()
        tao_mon_hoc()
        tao_quan_tri()
        tao_hoc_sinh()
        tao_hoc_ky()
        
        ### Tạo lớp học và xếp các học sinh vào lớp ở năm học 21
        print("Khởi tạo dữ liệu học sinh và danh sách lớp trong năm học 21")
        tao_lop_hoc_nam_21()
        tao_hoc_sinh_lop_nam_21()
        
        ### Tạo học kỳ mới: 22, 23, 24 
        print("Tạo các học kỳ mới")
        HocKy.nam_hoc_moi()
        HocKy.nam_hoc_moi()
        HocKy.nam_hoc_moi()
        
        ### Sau khi đã có học kỳ mới, tạo lớp xếp các học sinh còn lại
        print("Khởi tạo dữ liệu học sinh và danh sách lớp trong các năm học còn lại")
        tao_lop_hoc_va_hoc_sinh_lop_con_lai()
        
        ### Phân môn giáo viên dạy
        print("Phân công môn giáo viên")
        phan_mon_giao_vien()
        phan_lop_giao_vien()
        
        # Tạo bảng điểm
        print("Tạo bảng điểm, rất nhiều bảng điểm, quá trình này có thể mất 30 phút")
        print("Tạo dữ liệu bảng điểm, hơn 10000 bảng điểm nên hơi lâu")
        tao_bang_diem()
        print("Tạo chèn số điểm, hơn 10000 điểm 15 phút và 10000 điểm một tiết nên hơi lâu")
        cap_nhat_diem()
        
        db.session.commit()
        print('Tạo dữ liệu mẫu thành công')
import json
import hashlib
import os

from app import app, db
from models import MonHoc, GiaoVien, QuanTri

# Lấy đường dẫn của thư mục hiện tại
script_dir = os.path.dirname(__file__)

# Khởi tạo đường dẫn tuyệt đối cho các tệp json
giao_vien_path = os.path.join(script_dir, 'giaovien.json')
mon_hoc_path = os.path.join(script_dir, 'monhoc.json')
quan_tri_path = os.path.join(script_dir, 'quantri.json')

if __name__ == '__main__':
    print("Importing app and models in seed.py")

    print("Imported successfully!")
    
    with app.app_context():
        db.create_all()

        # Tạo GiaoVien
        with open(giao_vien_path, 'r', encoding= 'utf-8') as file:
            data = json.load(file)
            for item in data:
                giao_vien = GiaoVien(
                    username=item['username'],
                    password=item['password'],
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
        
        # Tạo MonHoc
        with open(mon_hoc_path, 'r', encoding= 'utf-8') as file:
            data = json.load(file)
            for item in data:
                mon_hoc = MonHoc(
                    ten_mon_hoc=item['ten_mon_hoc']
                )
                db.session.add(mon_hoc)
            db.session.commit()
            
        # Tạo QuanTri
        with open(quan_tri_path, 'r', encoding= 'utf-8') as file:
            data = json.load(file)
            for item in data:
                quan_tri = QuanTri(
                    username=item['username'],
                    password=item['password'],
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
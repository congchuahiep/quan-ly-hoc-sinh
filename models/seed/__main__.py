import json
import hashlib
from app import app, db
from models import GiaoVien, MonHoc

import os

# Lấy đường dẫn của thư mục hiện tại
script_dir = os.path.dirname(__file__)

# Khởi tạo đường dẫn tuyệt đối cho các tệp json
giao_vien_path = os.path.join(script_dir, 'giaovien.json')
mon_hoc_path = os.path.join(script_dir, 'monhoc.json')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Tạo GiaoVien
        with open(giao_vien_path, 'r') as file:
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
        
        with open(mon_hoc_path, 'r') as file:
            data = json.load(file)
            for item in data:
                mon_hoc = MonHoc(
                    ten_mon_hoc=item['ten_mon_hoc']
                )
                db.session.add(mon_hoc)
            db.session.commit()
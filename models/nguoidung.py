import hashlib
from flask_login import UserMixin
from sqlalchemy import Column, Date, Enum, Integer, String

from app import db


class NguoiDung(db.Model, UserMixin):
    __tablename__ = 'NguoiDung'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password = Column(String(256))
    ten = Column(String(50))
    ho = Column(String(120))
    ngay_sinh = Column(Date)
    email = Column(String(50))
    dien_thoai = Column(String(15))
    dia_chi = Column(String(50))
    gioi_tinh = Column(Enum('Nam', 'Nu'))
    loai_nguoi_dung = Column(Enum('NhanVien', 'GiaoVien', 'QuanTri'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'NguoiDung',
        'polymorphic_on': loai_nguoi_dung
    }

    def __init__(self, username, password, ten, ho, ngay_sinh, email, dien_thoai, dia_chi, gioi_tinh, loai_nguoi_dung):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.ten = ten
        self.ho = ho
        self.ngay_sinh = ngay_sinh
        self.email = email
        self.dien_thoai = dien_thoai
        self.dia_chi = dia_chi
        self.gioi_tinh = gioi_tinh
        self.loai_nguoi_dung = loai_nguoi_dung
        
    def check_loai_nguoi_dung(self, loai_nguoi_dung: str):
        return self.loai_nguoi_dung == loai_nguoi_dung
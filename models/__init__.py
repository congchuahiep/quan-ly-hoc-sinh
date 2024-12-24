import hashlib
from sqlalchemy import Column, Enum, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from app import db

day_mon = db.Table('DayMon', 
    Column('giao_vien_id', Integer, ForeignKey('GiaoVien.id'), primary_key=True),
    Column('mon_hoc_id', Integer, ForeignKey('MonHoc.id'), primary_key=True)
)


class NguoiDung(db.Model, UserMixin):
    __tablename__ = 'NguoiDung'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    avatar = Column(String(120), nullable=True)
    ten = Column(String(50), nullable=False)
    ho = Column(String(120), nullable=False)
    ngay_sinh = Column(Date, nullable=False)
    email = Column(String(50), nullable=False)
    dien_thoai = Column(String(15), nullable=False)
    dia_chi = Column(String(50), nullable=False)
    gioi_tinh = Column(Enum('Nam', 'Nu'), nullable=False)
    loai_nguoi_dung = Column(Enum('NhanVien', 'GiaoVien', 'QuanTri'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'NguoiDung',
        'polymorphic_on': loai_nguoi_dung
    }
    
    def __str__(self):
        return self.username

    def __init__(self, username, password, avatar, ten, ho, ngay_sinh, email, dien_thoai, dia_chi, gioi_tinh, loai_nguoi_dung):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.avatar = avatar
        self.ten = ten
        self.ho = ho
        self.ngay_sinh = ngay_sinh
        self.email = email
        self.dien_thoai = dien_thoai
        self.dia_chi = dia_chi
        self.gioi_tinh = gioi_tinh
        self.loai_nguoi_dung = loai_nguoi_dung
        
    def get_basic_info(self):
        return {
            'fullname': self.ho + ' ' + self.ten,
            'avatar': self.avatar,
            'role': self.get_role()
        }
        
    def check_loai_nguoi_dung(self, loai_nguoi_dung: str):
        return self.loai_nguoi_dung == loai_nguoi_dung
        
    
class GiaoVien(NguoiDung):
    __tablename__ = 'GiaoVien'
    id = Column(Integer, ForeignKey('NguoiDung.id'), primary_key=True)

    lop_chu_nhiem = relationship('LopHoc', uselist=False, back_populates='giao_vien_chu_nhiem')
    lop_giao_vien_day = relationship('DayLop', back_populates='giao_vien')
    day_mon = relationship('MonHoc', secondary=day_mon, back_populates='giao_viens')
    
    __mapper_args__ = {
        'polymorphic_identity': 'GiaoVien',
    }
    
    def get_nav_item_by_role(self):
        return [
                {'href': 'dashboard', 'icon': '<i class="bi bi-grid me-2"></i>', 'title': 'Tổng quan'},
                {'href': 'score', 'icon': '<i class="bi bi-book me-2"></i>', 'title': 'Quản lý bảng điểm'},
                {'href': 'login', 'icon': '', 'title': 'Setting'},
        ]
    
    def get_dashboard_data(self):
        return []
    
    def get_role(self):
        return "Giáo viên"


class NhanVien(NguoiDung):
    __tablename__ = 'NhanVien'
    id = Column(Integer, ForeignKey('NguoiDung.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'NhanVien',
    }
    

    
    def get_dashboard_data(self):
        
        total_hoc_sinh = db.session.query(HocSinh).count()
        total_giao_vien = db.session.query(GiaoVien).count()
        total_nhan_vien = db.session.query(NhanVien).count()
        ti_le_dat = str(100) + "%"
        
        return [
            {'title': 'Học sinh', 'value': total_hoc_sinh, 'icon': '<i class="bi bi-person fs-2"></i>'},
            {'title': 'Giáo viên', 'value': total_giao_vien, 'icon': '<i class="bi bi-person-workspace fs-2"></i>'},
            {'title': 'Nhân viên', 'value': total_nhan_vien, 'icon': '<i class="bi bi-briefcase fs-2"></i>'},
            {'title': 'Tỉ lệ đạt', 'value': ti_le_dat, 'icon': '<i class="bi bi-bar-chart-line fs-2"></i>'}
        ]
    
    def get_nav_item_by_role(self):
        return [
                {'href': 'dashboard', 'icon': '<i class="bi bi-grid me-2"></i>', 'title': 'Tổng quan'},
                {'href': 'login', 'icon': '', 'title': 'Contact'},
                {'href': 'login', 'icon': '', 'title': 'Setting'},
        ]
    
    def get_role(self):
        return "Nhân viên"


class QuanTri(NguoiDung):
    __tablename__ = 'QuanTri'
    id = Column(Integer, ForeignKey('NguoiDung.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'QuanTri',
    }
    
    def get_dashboard_data(self):
        
        total_hoc_sinh = db.session.query(HocSinh).count()
        total_giao_vien = db.session.query(GiaoVien).count()
        total_nhan_vien = db.session.query(NhanVien).count()
        ti_le_dat = str(100) + "%"
        
        return [
            {'title': 'Học sinh', 'value': total_hoc_sinh, 'icon': '<i class="bi bi-person fs-2"></i>'},
            {'title': 'Giáo viên', 'value': total_giao_vien, 'icon': '<i class="bi bi-person-workspace fs-2"></i>'},
            {'title': 'Nhân viên', 'value': total_nhan_vien, 'icon': '<i class="bi bi-briefcase fs-2"></i>'},
            {'title': 'Tỉ lệ đạt', 'value': ti_le_dat, 'icon': '<i class="bi bi-bar-chart-line fs-2"></i>'}
        ]
    
    def get_nav_item_by_role(self):
        return [
                {'href': 'dashboard', 'icon': '<i class="bi bi-grid me-2"></i>', 'title': 'Tổng quan'},
                {'href': 'login', 'icon': '', 'title': 'Contact'},
                {'href': 'login', 'icon': '', 'title': 'Setting'},
        ]
        
    def get_role(self):
        return "Quản trị"


class LopHoc(db.Model):
    __tablename__ = 'LopHoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_lop = Column(String(5))
    so_phong = Column(String(5))
    khoi_lop = Column(Enum('Khoi10', 'Khoi11', 'Khoi12'))
    giao_vien_chu_nhiem_id = Column(ForeignKey('GiaoVien.id'))

    giao_vien_chu_nhiem = relationship('GiaoVien', back_populates='lop_chu_nhiem')
    giao_vien_day_lop = relationship('DayLop', back_populates='lop_hoc')
    hoc_sinhs = relationship('HocSinhLop', back_populates='lop_hoc', lazy=True)


class DayLop(db.Model):
    __tablename__ = 'DayLop'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lop_hoc_id = Column(ForeignKey('LopHoc.id'))
    giao_vien_id = Column(ForeignKey('GiaoVien.id'))
    hoc_ky_id = Column(ForeignKey('HocKy.id'))
    mon_hoc_id = Column(ForeignKey('MonHoc.id'))

    lop_hoc = relationship('LopHoc', back_populates='giao_vien_day_lop', lazy='subquery')
    giao_vien = relationship('GiaoVien', back_populates='lop_giao_vien_day', lazy='subquery')
    hoc_ky = relationship('HocKy', lazy='subquery')
    mon_hoc = relationship('MonHoc', lazy='subquery')


class HocSinh(db.Model):
    __tablename__ = 'HocSinh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50))
    ngay_sinh = Column(Date)
    email = Column(String(50))
    dien_thoai = Column(String(15))
    dia_chi = Column(String(100))
    gioi_tinh = Column(Enum('Nam', 'Nu'))
    
    lich_su_lop_hoc = relationship('HocSinhLop', back_populates='hoc_sinh', lazy=True)
    bang_diems = relationship('BangDiem', back_populates='hoc_sinh', lazy=True)


class HocSinhLop(db.Model):
    __tablename__ = 'HocSinhLop'
    hoc_sinh_id = Column(Integer, ForeignKey('HocSinh.id'), primary_key=True)
    lop_hoc_id = Column(Integer, ForeignKey('LopHoc.id'), primary_key=True)
    ngay_bat_dau = Column(Date, primary_key=True)
    ngay_ket_thuc = Column(Date)
    trang_thai = Column(Enum('DangHoc', 'DaNghiHoc', 'ChuyenTruong', 'ChuyenLop', 'HocXong'))

    hoc_sinh = relationship('HocSinh', back_populates='lich_su_lop_hoc', lazy="subquery")
    lop_hoc = relationship('LopHoc', back_populates='hoc_sinhs', lazy="subquery")
    

class MonHoc(db.Model):
    __tablename__ = 'MonHoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_mon_hoc = Column(String(50))

    bang_diems = relationship('BangDiem', back_populates='mon_hoc', lazy=True)
    giao_viens = relationship('GiaoVien', secondary=day_mon, back_populates='day_mon')
    thong_ke_mon_hocs = relationship('ThongKeMonHoc', back_populates='mon_hoc', lazy=True)

    def __init__(self, ten_mon_hoc):
        self.ten_mon_hoc = ten_mon_hoc


class HocKy(db.Model):
    __tablename__ = 'HocKy'
    id = Column(Integer, primary_key=True)

    bang_diem = relationship('BangDiem', back_populates='hoc_ky', lazy=True)
    thong_ke_mon_hocs = relationship('ThongKeMonHoc', back_populates='hoc_ky', lazy=True)


class BangDiem(db.Model):
    __tablename__ = 'BangDiem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoc_sinh_id = Column(ForeignKey('HocSinh.id'))
    mon_hoc_id = Column(ForeignKey('MonHoc.id'))
    hoc_ky_id = Column(ForeignKey('HocKy.id'))
    diem_cuoi_ky = Column(Float)

    hoc_sinh = relationship('HocSinh', back_populates='bang_diems', lazy='subquery')
    mon_hoc = relationship('MonHoc', back_populates='bang_diems', lazy='subquery')
    hoc_ky = relationship('HocKy', back_populates='bang_diem', lazy='subquery')
    diem_15_phuts = relationship('Diem15Phut', back_populates='bang_diems', lazy=True)
    diem_mot_tiets = relationship('DiemMotTiet', back_populates='bang_diems', lazy=True)
    

class Diem15Phut(db.Model):
    __tablename__ = 'Diem15Phut'
    id = Column(Integer, primary_key=True, autoincrement=True)
    diem = Column(Float)
    bang_diem_id = Column(Integer, ForeignKey('BangDiem.id'))

    bang_diems = relationship('BangDiem', back_populates='diem_15_phuts', lazy=True)


class DiemMotTiet(db.Model):
    __tablename__ = 'DiemMotTiet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    diem = Column(Float)
    bang_diem_id = Column(Integer, ForeignKey('BangDiem.id'))

    bang_diems = relationship('BangDiem', back_populates='diem_mot_tiets', lazy=True)


class ThongKeMonHoc(db.Model):
    __tablename__ = 'ThongKeMonHoc'
    mon_hoc_id = Column(ForeignKey('MonHoc.id'), primary_key=True)
    hoc_ky_id = Column(ForeignKey('HocKy.id'), primary_key=True)
    tong_hoc_sinh = Column(Integer)
    tong_dat = Column(Integer)
    ti_le_dat = Column(Float)

    mon_hoc = relationship('MonHoc', back_populates='thong_ke_mon_hocs', lazy='subquery')
    hoc_ky = relationship('HocKy', back_populates='thong_ke_mon_hocs', lazy='subquery')
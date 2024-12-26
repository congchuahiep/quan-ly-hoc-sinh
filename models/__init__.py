from datetime import date
from enum import Enum as PyEnum
import hashlib
import random
from sqlalchemy import Column, Enum, Integer, String, Float, ForeignKey, Date, extract
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from app import db
from app.utils import chia_cac_phan_ngau_nhien, get_hoc_ky, get_nam_sinh

day_mon = db.Table('DayMon', 
    Column('giao_vien_id', Integer, ForeignKey('GiaoVien.id'), primary_key=True),
    Column('mon_hoc_id', Integer, ForeignKey('MonHoc.id'), primary_key=True)
)

lop_hoc_ky = db.Table('LopHocKy', 
    Column('lop_hoc_id', String(5), ForeignKey('LopHoc.id'), primary_key=True),
    Column('hoc_ky_id', Integer, ForeignKey('HocKy.id'), primary_key=True)
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
    
    @staticmethod
    def tim_giao_vien_khong_chu_nhiem(nam_hoc):
        return GiaoVien.query.filter(
                ~GiaoVien.lop_chu_nhiem.has(LopHoc.nam_hoc == nam_hoc)
            ).all()


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
    
    
class KhoiLop(PyEnum):
    Khoi10 = 10
    Khoi11 = 11
    Khoi12 = 12


class LopHoc(db.Model):
    __tablename__ = 'LopHoc'
    id = Column(String(5), primary_key=True)
    nam_hoc = Column(Integer)
    ten_lop = Column(String(5))
    khoi_lop = Column(Enum(KhoiLop))
    giao_vien_chu_nhiem_id = Column(ForeignKey('GiaoVien.id'))
    
    hai_hoc_ky = relationship('HocKy', secondary=lop_hoc_ky, back_populates='cac_lop_hoc', lazy='subquery')
    giao_vien_chu_nhiem = relationship('GiaoVien', back_populates='lop_chu_nhiem')
    giao_vien_day_lop = relationship('DayLop', back_populates='lop_hoc')
    hoc_sinhs = relationship('HocSinhLop', back_populates='lop_hoc', lazy=True)
    
    def __init__(self, id, ten_lop, nam_hoc, khoi_lop, giao_vien_chu_nhiem_id):
        self.id = id
        self.ten_lop = ten_lop
        self.nam_hoc = nam_hoc
        self.khoi_lop = khoi_lop
        self.giao_vien_chu_nhiem_id = giao_vien_chu_nhiem_id
        
    def tach_ten_lop(self):
        phan_so = int(''.join(filter(str.isdigit, self.ten_lop)))  # Lấy phần số
        phan_chu = ''.join(filter(str.isalpha, self.ten_lop))  # Lấy phần chữ
        
        return (phan_so, phan_chu)
     
    def get_danh_sach_hoc_sinh(self, trang_thai="DangHoc"):
        return HocSinhLop.query.filter(HocSinhLop.lop_hoc_id == self.id, HocSinhLop.trang_thai == trang_thai).all()
    
    @staticmethod
    def them_cac_hoc_sinh_vao_lop(lop_hoc, hoc_sinhs, ngay_bat_dau=date.today()):
        # Thêm học sinh vào lớp
        for hoc_sinh in hoc_sinhs:
            hoc_sinh_lop = HocSinhLop(
                hoc_sinh_id=hoc_sinh.id,
                lop_hoc_id=lop_hoc.id,
                ngay_bat_dau=ngay_bat_dau,  # Ngày bắt đầu học
                trang_thai="DangHoc"
            )
            db.session.add(hoc_sinh_lop)
    
    @staticmethod
    def xep_lop(nam_hoc, khoi_lop=10):
        # Truy vấn các học sinh và các lớp
        full_hoc_sinhs = HocSinh.query.filter(extract('year', HocSinh.ngay_sinh) == get_nam_sinh(nam_hoc, khoi_lop)).all()
        lop_hocs = LopHoc.query.filter(LopHoc.hai_hoc_ky.any(HocKy.nam_hoc == nam_hoc), LopHoc.khoi_lop == KhoiLop(khoi_lop)).all()
        
        if (len(lop_hocs) == 0):
            raise ValueError("Không còn lớp nào trống để xếp!")
        
        so_luong_lop = len(lop_hocs)
        
        # Cắt danh sách học sinh thành các phần
        si_so_tung_lop = chia_cac_phan_ngau_nhien(len(full_hoc_sinhs), so_luong_lop, 33, 40)
        index = 0
        
        for i in range(so_luong_lop):
            LopHoc.them_cac_hoc_sinh_vao_lop(lop_hoc=lop_hocs[i], hoc_sinhs=full_hoc_sinhs[index:index + si_so_tung_lop[i]])
            index += si_so_tung_lop[i]
            
    @staticmethod
    def tao_khoi_10_moi(nam_hoc, so_luong=5):
        cac_giao_vien_chu_nhiem = GiaoVien.tim_giao_vien_khong_chu_nhiem(nam_hoc-1)
        
        if (len(cac_giao_vien_chu_nhiem) < so_luong):
            raise ValueError("Không còn đủ giáo viên để xếp lớp!")
        
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
        
    def phan_cong_ngau_nhien_giao_vien_day_hoc(self):
        lop_hoc = self
        nam_hoc = lop_hoc.nam_hoc
        so_mon_hoc = MonHoc.query.count()
        
        (hoc_ky_mot, hoc_ky_hai) = get_hoc_ky(nam_hoc)

        #### 1. Phân công giáo viên chủ nhiệm
        giao_vien_chu_nhiem = GiaoVien.query.get(lop_hoc.giao_vien_chu_nhiem_id)
        
        # Chọn môn học ngẫu nhiên mà giáo viên chủ nhiệm dạy
        mon_hoc = random.choice(giao_vien_chu_nhiem.day_mon)
        
        day_lop_ky_mot = DayLop(
            lop_hoc_id = lop_hoc.id,
            giao_vien_id = lop_hoc.giao_vien_chu_nhiem_id,
            mon_hoc_id = mon_hoc.id,
            hoc_ky_id = hoc_ky_mot
        )
        
        day_lop_ky_hai = DayLop(
            lop_hoc_id = lop_hoc.id,
            giao_vien_id = lop_hoc.giao_vien_chu_nhiem_id,
            mon_hoc_id = mon_hoc.id,
            hoc_ky_id = hoc_ky_hai
        )
        
        db.session.add_all([day_lop_ky_mot, day_lop_ky_hai])
        db.session.commit()
            
        ### 2. Phân công thêm các giáo viên và môn học còn lại
        # Lấy danh sách các giáo viên trừ giáo viên đã dạy
        giao_vien_da_phan_cong_id = {gv.id for gv in lop_hoc.giao_vien_day_lop}
        # Lấy danh sách các môn học đã có
        mon_hoc_da_co_id = {gv_lh.mon_hoc_id for gv_lh in lop_hoc.giao_vien_day_lop}
        
        while len(mon_hoc_da_co_id) < so_mon_hoc:
            # Lọc môn học còn thiếu
            mon_hoc_con_thieu = MonHoc.query.filter(~MonHoc.id.in_(mon_hoc_da_co_id)).first()
            
            # Lọc danh sách các giáo viên dạy môn học còn thiếu
            giao_viens = GiaoVien.query.filter(GiaoVien.day_mon.any(MonHoc.id == mon_hoc_con_thieu.id)).all()
            # Lọc danh sách các giáo viên đã dạy lớp này
            giao_viens = GiaoVien.query.filter(~GiaoVien.id.in_(giao_vien_da_phan_cong_id)).all()
            giao_vien = random.choice(giao_viens)
            
            day_lop_ky_mot = DayLop(
                lop_hoc_id = lop_hoc.id,
                giao_vien_id = giao_vien.id,
                mon_hoc_id = mon_hoc_con_thieu.id,
                hoc_ky_id = hoc_ky_mot
            )
            
            day_lop_ky_hai = DayLop(
                lop_hoc_id = lop_hoc.id,
                giao_vien_id = giao_vien.id,
                mon_hoc_id = mon_hoc_con_thieu.id,
                hoc_ky_id = hoc_ky_hai
            )
            
            db.session.add_all([day_lop_ky_mot, day_lop_ky_hai])
            
            giao_vien_da_phan_cong_id.add(giao_vien.id)
            mon_hoc_da_co_id.add(mon_hoc_con_thieu.id)
            db.session.commit()
    
    def len_lop(self, ngay_bat_dau=date.today()):
        khoi_lop, loai_lop = self.tach_ten_lop()
        nam_hoc_cu = self.nam_hoc
        nam_hoc_moi = nam_hoc_cu + 1
        
        if not HocKy.query.get(nam_hoc_moi * 10 + 1):
            print("Năm học mới không có trong hệ thống")
            return None
        
        danh_sach_hoc_sinh = self.get_danh_sach_hoc_sinh()
        
        if khoi_lop == 12:
            
            for hoc_sinh_lop in danh_sach_hoc_sinh:
                hoc_sinh_lop.trang_thai = "HocXong"
            
            # TODO: thêm khả năng kết thúc cấp ba
            return None
        
        ten_lop_moi = str(khoi_lop + 1) + loai_lop
        (hoc_ky_mot_moi, hoc_ky_hai_moi) = HocKy.get_hoc_ky(nam_hoc_moi)
        
        print(self.id, " -> ", str(nam_hoc_moi) + ten_lop_moi)
        
        lop_moi = LopHoc(
            id=str(nam_hoc_moi) + ten_lop_moi,
            nam_hoc=nam_hoc_moi,
            ten_lop=ten_lop_moi,
            khoi_lop=KhoiLop(khoi_lop),
            giao_vien_chu_nhiem_id=self.giao_vien_chu_nhiem_id
        )
        lop_moi.hai_hoc_ky.append(hoc_ky_mot_moi)
        lop_moi.hai_hoc_ky.append(hoc_ky_hai_moi)
        
        db.session.add(lop_moi)
        
        
        for hoc_sinh_lop in danh_sach_hoc_sinh:
            hoc_sinh_lop.trang_thai = "HocXong"
            
            hoc_sinh = HocSinh.query.get(hoc_sinh_lop.hoc_sinh_id)
            
            hoc_sinh_lop = HocSinhLop(
                hoc_sinh_id = hoc_sinh.id,
                lop_hoc_id = lop_moi.id,
                ngay_bat_dau = ngay_bat_dau,
                trang_thai = "DangHoc"
            )
            db.session.add(hoc_sinh_lop)
            
        db.session.commit()


class DayLop(db.Model):
    __tablename__ = 'DayLop'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lop_hoc_id = Column(ForeignKey('LopHoc.id'))
    giao_vien_id = Column(ForeignKey('GiaoVien.id'))
    hoc_ky_id = Column(ForeignKey('HocKy.id'))
    mon_hoc_id = Column(ForeignKey('MonHoc.id'))

    lop_hoc = relationship('LopHoc', back_populates='giao_vien_day_lop', lazy='subquery')
    giao_vien = relationship('GiaoVien', back_populates='lop_giao_vien_day', lazy='subquery')
    hoc_ky = relationship('HocKy', back_populates='cac_giao_vien', lazy='subquery')
    mon_hoc = relationship('MonHoc', lazy='subquery')


class HocSinh(db.Model):
    __tablename__ = 'HocSinh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50))
    ho = Column(String(120))
    ngay_sinh = Column(Date)
    email = Column(String(50))
    dien_thoai = Column(String(15))
    dia_chi = Column(String(100))
    gioi_tinh = Column(Enum('Nam', 'Nu'))
    
    lich_su_lop_hoc = relationship('HocSinhLop', back_populates='hoc_sinh', lazy=True)
    bang_diems = relationship('BangDiem', back_populates='hoc_sinh', lazy=True)
    
    def __init__(self, ten, ho, ngay_sinh, email, dien_thoai, dia_chi, gioi_tinh):
        self.ten = ten
        self.ho = ho
        self.ngay_sinh = ngay_sinh
        self.email = email
        self.dien_thoai = dien_thoai
        self.dia_chi = dia_chi
        self.gioi_tinh = gioi_tinh


class HocSinhLop(db.Model):
    __tablename__ = 'HocSinhLop'
    hoc_sinh_id = Column(Integer, ForeignKey('HocSinh.id'), primary_key=True)
    lop_hoc_id = Column(String(5), ForeignKey('LopHoc.id'), primary_key=True)
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
    
    cac_lop_hoc = relationship('LopHoc', secondary=lop_hoc_ky, back_populates='hai_hoc_ky', lazy='subquery')
    cac_giao_vien = relationship('DayLop', back_populates='hoc_ky', lazy=True)
    bang_diem = relationship('BangDiem', back_populates='hoc_ky', lazy=True)
    thong_ke_mon_hocs = relationship('ThongKeMonHoc', back_populates='hoc_ky', lazy=True)
    
    def __init__(self, id):
        self.id = id
        
    @staticmethod
    def nam_hoc_moi():
        nam_hoc_cu = HocKy.query.order_by(HocKy.id.desc()).first().nam_hoc
        nam_hoc_moi = nam_hoc_cu + 1
        hoc_ky_mot = HocKy(id=nam_hoc_moi * 10 + 1)
        hoc_ky_hai = HocKy(id=nam_hoc_moi * 10 + 2)
        
        db.session.add_all([hoc_ky_mot, hoc_ky_hai])
        db.session.commit()
    
    @staticmethod
    def get_hoc_ky(nam_hoc):
        hoc_ky_mot = HocKy.query.get(nam_hoc * 10 + 1)
        hoc_ky_hai = HocKy.query.get(nam_hoc * 10 + 2)
        
        return (hoc_ky_mot, hoc_ky_hai)
    
    @hybrid_property
    def nam_hoc(self):
        return self.id // 10


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
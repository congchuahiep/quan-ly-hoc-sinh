from sqlalchemy import Column, Enum, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app import app, db

class NguoiDung(db.Model):
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
    loai_nguoi_dung = Column(Enum('NhanVien', 'GiaoVien', 'QuanTri'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'NguoiDung',
        'polymorphic_on': loai_nguoi_dung
    }
    
class GiaoVien(NguoiDung):
    __tablename__ = 'GiaoVien'
    id = Column(Integer, ForeignKey('NguoiDung.id'), primary_key=True)
    
    lop_chu_nhiem = relationship('LopHoc', uselist=False, back_populates='giao_vien_chu_nhiem')
    day_lop = relationship('LopHoc', secondary='DayLop', back_populates='giao_viens')
    day_mon = relationship('MonHoc', secondary='day_mon', back_populates='giao_viens')
    
    __mapper_args__ = {
        'polymorphic_identity': 'GiaoVien',
    }

class NhanVien(NguoiDung):
    __tablename__ = 'NhanVien'
    id = Column(Integer, ForeignKey('NguoiDung.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'NhanVien',
    }

class QuanTri(NguoiDung):
    __tablename__ = 'QuanTri'
    id = Column(Integer, ForeignKey('NguoiDung.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'QuanTri',
    }

day_mon = db.Table('DayMon', 
    Column('giao_vien_id', Integer, ForeignKey('GiaoVien.id'), primary_key=True),
    Column('mon_hoc_id', Integer, ForeignKey('MonHoc.id'), primary_key=True)
)
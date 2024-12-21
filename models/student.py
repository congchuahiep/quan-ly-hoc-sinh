from sqlalchemy import Column, Enum, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app import app, db

class HocSinh(db.Model):
    __tablename__ = 'HocSinh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50))
    ngay_sinh = Column(Date)
    email = Column(String(50))
    dien_thoai = Column(String(15))
    dia_chi = Column(String(100))
    gioi_tinh = Column(Enum('Nam', 'Nu'))
    
    lich_su_lop_hoc = relationship('LopHoc', secondary='hoc_sinh_lop', back_populates='hoc_sinhs')
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
    
from sqlalchemy import Column, Enum, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app import app, db

class LopHoc(db.Model):
    __tablename__ = 'LopHoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_lop = Column(String(5))
    so_phong = Column(String(5))
    khoi_lop = Column(Enum('Khoi10', 'Khoi11', 'Khoi12'))
    giao_vien_chu_nhiem_id = Column(ForeignKey('GiaoVien.id'))

    giao_vien_chu_nhiem = relationship('GiaoVien', back_populates='lop_chu_nhiem')
    giao_viens = relationship('GiaoVien', secondary='day_lop', back_populates='day_lop')
    hoc_sinhs = relationship('HocSinh', secondary='hoc_sinh_lop', back_populates='lop_hocs')


class DayLop(db.Model):
    __tablename__ = 'DayLop'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lop_hoc_id = Column(ForeignKey('LopHoc.id'))
    giao_vien_id = Column(ForeignKey('GiaoVien.id'))
    hoc_ky_id = Column(ForeignKey('HocKy.id'))
    mon_hoc_id = Column(ForeignKey('MonHoc.id'))

    lop_hoc = relationship('LopHoc', back_populates='giao_viens', lazy='subquery')
    giao_vien = relationship('GiaoVien', back_populates='day_lop', lazy='subquery')
    hoc_ky = relationship('HocKy', lazy='subquery')
    mon_hoc = relationship('MonHoc', lazy='subquery')
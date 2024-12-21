from sqlalchemy import Column, Enum, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app import app, db

class MonHoc(db.Model):
    __tablename__ = 'MonHoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_mon_hoc = Column(String(50))
    so_tiet = Column(Integer)

    bang_diems = relationship('BangDiem', back_populates='mon_hoc', lazy=True)
    giao_viens = relationship('GiaoVien', secondary='day_mon', back_populates='day_mon')
    thong_ke_mon_hocs = relationship('ThongKeMonHoc', back_populates='mon_hoc', lazy=True)

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
    diem_15_phuts = relationship('Diem15Phut', back_populates='bang_diem', lazy=True)
    diem_mot_tiets = relationship('DiemMotTiet', back_populates='bang_diem', lazy=True)
    

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

    bang_diem = relationship('BangDiem', back_populates='diem_mot_tiets', lazy=True)


class ThongKeMonHoc(db.Model):
    __tablename__ = 'ThongKeMonHoc'
    mon_hoc_id = Column(ForeignKey('MonHoc.id'), primary_key=True)
    hoc_ky_id = Column(ForeignKey('HocKy.id'), primary_key=True)
    tong_hoc_sinh = Column(Integer)
    tong_dat = Column(Integer)
    ti_le_dat = Column(Float)

    mon_hoc = relationship('MonHoc', back_populates='thong_ke_mon_hocs', lazy='subquery')
    hoc_ky = relationship('HocKy', back_populates='thong_ke_mon_hocs', lazy='subquery')
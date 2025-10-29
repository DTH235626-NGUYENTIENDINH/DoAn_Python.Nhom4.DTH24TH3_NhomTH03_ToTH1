CREATE DATABASE QuanLySach
ON PRIMARY
(
    NAME = N'QuanLySach_Data',
    FILENAME = N'D:\Inclass_Sources\Python\DoAn_Python.Nhom4.DTH24TH3_NhomTH03_ToTH1\Database\QuanLySach.mdf',
    SIZE = 10MB,
    FILEGROWTH = 5MB
)
LOG ON
(
    NAME = N'QuanLySach_Log',
    FILENAME = N'D:\Inclass_Sources\Python\DoAn_Python.Nhom4.DTH24TH3_NhomTH03_ToTH1\Database\QuanLySach_log.ldf',
    SIZE = 10MB,
    FILEGROWTH = 5MB
);
use QuanLySach

drop table SACH
create table SACH(
	ID_Sach int identity(1,1) primary key,
	TenSach nvarchar(100) not null,
	TacGia nvarchar(100),
	TheLoai nvarchar(50),
	SoLuong int,
)

drop table NGUOIDUNG
create table NGUOIDUNG(
	ID_user int identity(1,1) primary key,
	HoTen nvarchar(100) not null,
	_Username nvarchar(16) not null unique,
	_Password nvarchar(100) not null,
	SDT nvarchar(15),
	User_Role int not null default 0
)

drop table PHIEUMUON
CREATE TABLE PHIEUMUON(
    ID_PhieuMuon INT IDENTITY(1,1) PRIMARY KEY,
    ID_user INT NOT NULL,
    NgayMuon DATETIME,
    NgayTra DATETIME NULL,
    TrangThai NVARCHAR(50) DEFAULT N'Chưa trả', 
    FOREIGN KEY (ID_user) REFERENCES NGUOIDUNG(ID_User),
    CONSTRAINT CHK_TrangThai CHECK (TrangThai IN (N'Chưa trả', N'Đã trả', N'Quá hạn'))
)

drop table CTPM 
create table CTPM(
	ID_Sach int not null,
	ID_PhieuMuon int not null,
	SoLuong_Muon int,
	PRIMARY KEY (ID_Sach, ID_PhieuMuon),
    FOREIGN KEY (ID_Sach) REFERENCES SACH(ID_Sach),
    FOREIGN KEY (ID_PhieuMuon) REFERENCES PHIEUMUON(ID_PhieuMuon)
)

select *from PHIEUMUON
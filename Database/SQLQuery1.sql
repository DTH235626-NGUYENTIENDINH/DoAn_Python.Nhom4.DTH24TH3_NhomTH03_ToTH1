CREATE DATABASE QuanLySach
ON PRIMARY
(
    NAME = QuanLySach_Data,
    FILENAME = 'D:\AGU\2025-2026_hoc_hi_1\Python\DoAn_QuanLySach\Database\QuanLySach.mdf',
    SIZE = 10MB,
    FILEGROWTH = 5MB
)
LOG ON
(
    NAME = QuanLySach_Log,
    FILENAME = 'D:\AGU\2025-2026_hoc_hi_1\Python\DoAn_QuanLySach\Database\QuanLySach_log.ldf',
    SIZE = 10MB,
    FILEGROWTH = 5MB
);
use QuanLySach

CREATE TABLE Sach (
    MaSach VARCHAR(7) PRIMARY KEY, -- Mã sách là 7 ký tự và là Khóa chính
    TenSach NVARCHAR(255) NOT NULL,
    TacGia NVARCHAR(100),
	LoaiSach NVARCHAR(50),
    NhaXuatBan NVARCHAR(100),
    NamXuatBan INT,
    SoLuongTonKho INT DEFAULT 0,    
    -- Ràng buộc 1: Kiểm tra độ dài Mã Sách phải là 7
    CONSTRAINT CK_Sach_MaSachLength 
        CHECK (LEN(MaSach) = 7),        
    -- Ràng buộc 2: Kiểm tra cấu trúc Mã Sách (2 Chữ A-Z | 2 Số | 3 Số)
    CONSTRAINT CK_Sach_MaSachStructure 
        CHECK (
            -- Kiểm tra 2 ký tự đầu (Phần LOẠI) là chữ cái in hoa (A-Z)
            SUBSTRING(MaSach, 1, 2) NOT LIKE '%[^A-Z]%' AND            
            -- Kiểm tra 2 ký tự tiếp theo (Phần NĂM) là số (0-9)
            SUBSTRING(MaSach, 3, 2) NOT LIKE '%[^0-9]%' AND            
            -- Kiểm tra 3 ký tự cuối (Phần STT) là số (0-9)
            SUBSTRING(MaSach, 5, 3) NOT LIKE '%[^0-9]%'
        )
);

CREATE TABLE DocGia (
    MaDocGia VARCHAR(6) PRIMARY KEY, -- Đã đổi độ dài thành 6
    HoTen NVARCHAR(100) NOT NULL,
    DiaChi NVARCHAR(255),
    SoDienThoai VARCHAR(15),
    NgaySinh DATE,
    
    -- Ràng buộc 1: Kiểm tra độ dài Mã Độc Giả phải là 6
    CONSTRAINT CK_DocGia_MaDocGiaLength 
        CHECK (LEN(MaDocGia) = 6),
        
    -- Ràng buộc 2: Kiểm tra cấu trúc Mã Độc Giả (DG + 4 Số)
    CONSTRAINT CK_DocGia_MaDocGiaStructure 
        CHECK (
            -- Kiểm tra 2 ký tự đầu phải là 'DG'
            SUBSTRING(MaDocGia, 1, 2) = 'DG' AND
            
            -- Kiểm tra 4 ký tự cuối (Phần STT) là số (0-9)
            SUBSTRING(MaDocGia, 3, 4) NOT LIKE '%[^0-9]%'
        )
);

CREATE TABLE PhieuMuon (
    MaMuonTra VARCHAR(10) PRIMARY KEY, -- Đã đổi độ dài thành 10
    MaDocGia VARCHAR(6) NOT NULL,
    NgayMuon DATETIME NOT NULL,
    TongSachMuon INT DEFAULT 0,
    
    -- Ràng buộc 1: Kiểm tra độ dài Mã Muon Tra phải là 10
    CONSTRAINT CK_PhieuMuon_MaMuonTraLength_10 
        CHECK (LEN(MaMuonTra) = 10),

    -- Ràng buộc 2: Kiểm tra cấu trúc Mã Muon Tra (6 Số cho Ngày + 4 Số cho STT)
    CONSTRAINT CK_PhieuMuon_MaMuonTraStructure_10
        CHECK (
            -- Kiểm tra 6 ký tự đầu (YYMMDD) là số
            SUBSTRING(MaMuonTra, 1, 6) NOT LIKE '%[^0-9]%' AND
            
            -- Kiểm tra 4 ký tự cuối (STT) là số
            SUBSTRING(MaMuonTra, 7, 4) NOT LIKE '%[^0-9]%'
        ),
        
    FOREIGN KEY (MaDocGia) REFERENCES DocGia(MaDocGia)
        ON UPDATE CASCADE 
        ON DELETE NO ACTION 
);

CREATE TABLE ChiTietMuonSach (
    MaMuonTra VARCHAR(10), -- Đã đổi độ dài thành 10
    MaSach VARCHAR(7),
    NgayTraDuKien DATE NOT NULL,
    NgayTraThucTe DATE,
    PhiPhat DECIMAL(10, 2) DEFAULT 0.00,
    TinhTrangSachKhiTra NVARCHAR(255),
    
    PRIMARY KEY (MaMuonTra, MaSach), 
    
    -- Khóa ngoại phải tham chiếu đến Mã Phiếu Mượn 10 ký tự
    FOREIGN KEY (MaMuonTra) REFERENCES PhieuMuon(MaMuonTra)
        ON UPDATE CASCADE 
        ON DELETE CASCADE, 
        
    FOREIGN KEY (MaSach) REFERENCES Sach(MaSach)
        ON UPDATE CASCADE
        ON DELETE NO ACTION 
);

CREATE TABLE NguoiDungHeThong (
    MaNguoiDung INT PRIMARY KEY IDENTITY(1,1),
    TenDangNhap VARCHAR(50) NOT NULL UNIQUE,
    MatKhauHash VARCHAR(255) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    HoTen NVARCHAR(100),
    -- Cột NgayTao đã được loại bỏ
    
    -- Ràng buộc cấu trúc Email cơ bản
    CONSTRAINT CK_NguoiDung_EmailFormat 
    CHECK (
        Email LIKE '%@%' AND 
        Email LIKE '%@%.%' AND
        Email NOT LIKE '@%' AND
        Email NOT LIKE '%@.%'
    )
);

drop table Sach
drop table DocGia
drop table PhieuMuon
drop table ChiTietMuonSach

select * from Sach
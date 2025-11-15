
from .db_connect import connect_to_db
from tkinter import messagebox, filedialog
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import datetime
import customtkinter as ctk
import os
EXPORT_FOLDER = "EXPORT_FOLDER"
def format_date_for_sql(date_str):
    # Xử lý chuỗi rỗng
    if not date_str or date_str.strip() == "" or date_str.strip() == "dd/mm/yyyy":
        return None 
    
    try:
        dt_obj = datetime.datetime.strptime(date_str.strip(), '%d/%m/%Y')
        
        return dt_obj.strftime('%Y-%m-%d')
        
    except ValueError:
        messagebox.showerror("Lỗi Định dạng Ngày", 
                             f"Ngày '{date_str}' không hợp lệ. Vui lòng sử dụng định dạng DD/MM/YYYY.")
        return None

def get_top_n_data(report_type, n_str, date_from_str, date_to_str):
    conn = connect_to_db()
    if conn is None:
        return None
    cursor = conn.cursor()
    try:
        n = int(n_str)
    except ValueError:
        n = 10
    date_from = format_date_for_sql(date_from_str)
    date_to = format_date_for_sql(date_to_str)

    date_clause = ""
    params = []

    if date_from and date_to:
        date_clause = "AND pm.NgayMuon BETWEEN ? AND ?"
        params = [date_from, date_to]
    elif date_from:
        date_clause = "AND pm.NgayMuon >= ?"
        params = [date_from]
    elif date_to:
        date_clause = "AND pm.NgayMuon <= ?"
        params = [date_to]

    order = "DESC"
    if "ít nhất" in report_type:
        order = "ASC"

    if "sách được mượn" in report_type:
        # Báo cáo Sách mượn nhiều/ít nhất
        sql_template = f"""
            SELECT TOP {n} S.TenSach, COUNT(C.MaSach) AS TotalMuon
            FROM ChiTietPhieuMuon AS C
            JOIN PhieuMuon AS pm ON C.MaPhieuMuon = pm.MaPhieuMuon
            JOIN Sach AS S ON C.MaSach = S.MaSach
            WHERE 1=1 {date_clause}
            GROUP BY S.TenSach
            ORDER BY TotalMuon {order};
        """
    elif "độc giả mượn" in report_type:
        # Báo cáo Độc giả mượn nhiều/ít nhất
        sql_template = f"""
            SELECT TOP {n} DG.HoTen, COUNT(pm.MaDocGia) AS TotalGiaoDich
            FROM PhieuMuon AS pm
            JOIN DocGia AS DG ON pm.MaDocGia = DG.MaDocGia
            WHERE 1=1 {date_clause}
            GROUP BY DG.HoTen
            ORDER BY TotalGiaoDich {order};
        """
    elif "số lượng tồn" in report_type:
        # Báo cáo Tồn kho (Không cần lọc theo ngày)
        sql_template = f"""
            SELECT TOP {n} TenSach, SoLuongTonKho
            FROM Sach
            ORDER BY SoLuongTonKho {order};
        """
        params = [] # Báo cáo tồn kho không dùng tham số ngày
    else:
        messagebox.showinfo("Thông báo", "Loại báo cáo chưa được hỗ trợ.")
        return None
    
    try:
        # Nếu params không rỗng (tức là có lọc ngày)
        if params:
            df = pd.read_sql(sql_template, conn, params=params)
        else:
            # Nếu params rỗng (tồn kho hoặc không có ngày tháng)
            df = pd.read_sql(sql_template, conn)
            
        return df
    except Exception as e:
        messagebox.showerror("Lỗi Truy vấn", f"Lỗi truy vấn SQL: {e}")
        return None
    finally:
        if conn:
            conn.close()

def generate_report_and_chart(report_type, n_str, date_from_str, date_to_str, frame_to_display):
    try:
        n = int(n_str)
    except ValueError:
        messagebox.showerror("Lỗi", "Giá trị Top N phải là một số nguyên.")
        return
    df = get_top_n_data(report_type, n_str, date_from_str, date_to_str)
    for widget in frame_to_display.winfo_children():
        widget.destroy()

    if df is None or df.empty:
        # Nếu không có dữ liệu, hiển thị thông báo
        ctk.CTkLabel(frame_to_display, 
                     text="Không tìm thấy dữ liệu phù hợp hoặc lỗi truy vấn.",
                     font=ctk.CTkFont(size=14)).pack(padx=20, pady=20)
        return
    
    # Lấy tên cột cho biểu đồ
    labels = df.iloc[:, 0] # Tên sách/độc giả
    values = df.iloc[:, 1] # Số lượng mượn/tồn kho  
    # Thiết lập Tiêu đề cột Y động (tên cột thứ 2 từ truy vấn SQL)
    y_label = df.columns[1]    
    # Tạo đối tượng Figure và Axes (Khung biểu đồ)
    fig, ax = plt.subplots(figsize=(8, 5)) 
    # Vẽ biểu đồ cột
    ax.bar(labels, values, color='#3C8EFA', width= 0.3)
    ax.set_title(f"{report_type} (Top {n})", fontsize=14)
    ax.set_ylabel(y_label)   
    # Tinh chỉnh X-axis (xoay nhãn)
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout()
    # Tạo canvas Matplotlib
    canvas = FigureCanvasTkAgg(fig, master=frame_to_display)   
    # Lấy widget Tkinter của canvas
    canvas_widget = canvas.get_tk_widget()   
    # Đặt widget vào Frame giao diện và làm cho nó giãn nở
    canvas_widget.pack(fill=tk.BOTH, expand=True)   
    # Vẽ biểu đồ
    canvas.draw()

def export_data_to_excel(report_type, n_str, date_from_str, date_to_str):
    
    # 1. Validation và Lấy Dữ liệu (Giữ nguyên)
    try:
        n = int(n_str)
    except ValueError:
        messagebox.showerror("Lỗi", "Giá trị Top N không hợp lệ.")
        return

    df = get_top_n_data(report_type, n_str, date_from_str, date_to_str)
    
    if df is None or df.empty:
        messagebox.showinfo("Thông báo", "Không có dữ liệu để xuất.")
        return

    # 2. XÂY DỰNG ĐƯỜNG DẪN CỐ ĐỊNH (FIXED PATH)
    
    # Đảm bảo thư mục "BaoCao" tồn tại
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)
    
    # Tạo tên file: Ví dụ: Top_sach_duoc_muon_nhieu_nhat_Top10.xlsx
    file_name = f"{report_type.replace(' ', '_').replace('á','a').replace('ớ','o')}_Top{n}.xlsx"
    file_path = os.path.join(EXPORT_FOLDER, file_name)

    # 3. Xuất dữ liệu
    try:
        # Sử dụng pandas để xuất DataFrame sang Excel
        df.to_excel(file_path, index=False, sheet_name="BaoCao")
        messagebox.showinfo("Thành công", f"Đã xuất báo cáo thành công tại thư mục:\n{os.path.abspath(EXPORT_FOLDER)}\n\nTên file: {file_name}")
        
    except Exception as e:
        messagebox.showerror("Lỗi Xuất file", f"Không thể lưu file Excel: {e}")


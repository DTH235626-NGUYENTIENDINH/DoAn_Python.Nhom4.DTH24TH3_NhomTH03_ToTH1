
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
import re
import bcrypt
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

import tkinter.simpledialog as simpledialog 
def export_data_to_excel(report_type, n_str, date_from_str, date_to_str):
    """
    Hàm này không còn mở hộp thoại Save As mà yêu cầu nhập tên file.
    """
    try:
        n = int(n_str)
    except ValueError:
        messagebox.showerror("Lỗi", "Giá trị Top N không hợp lệ.")
        return

    df = get_top_n_data(report_type, n_str, date_from_str, date_to_str)
    
    if df is None or df.empty:
        messagebox.showinfo("Thông báo", "Không có dữ liệu để xuất.")
        return
    
    # Mở hộp thoại nhập liệu Tkinter
    file_name = simpledialog.askstring(
        "Nhập Tên File", 
        "Nhập tên cho file Excel:", 
        # Tên gợi ý ban đầu
        initialvalue=f"BaoCao_{report_type.replace(' ', '_').replace('á','a').replace('ớ','o')}"
    )
    
    if not file_name:
        messagebox.showinfo("Thông báo", "Đã hủy thao tác xuất file.")
        return False
        
    # --- Đảm bảo thư mục tồn tại và tạo đường dẫn cố định ---
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)
        
    # Thêm đuôi .xlsx nếu người dùng quên
    if not file_name.lower().endswith('.xlsx'):
        file_name += '.xlsx'
        
    file_path = os.path.join(EXPORT_FOLDER, file_name)

    # 3. Xuất dữ liệu
    try:
        df.to_excel(file_path, index=False, sheet_name="BaoCao")
        messagebox.showinfo("Thành công", f"Đã xuất báo cáo thành công tại thư mục:\n{os.path.abspath(EXPORT_FOLDER)}")
        return True 
        
    except Exception as e:
        messagebox.showerror("Lỗi Xuất file", f"Không thể lưu file Excel: {e}")
        return False

def open_export_folder():
    """Mở thư mục chứa các file báo cáo."""
    abs_path = os.path.abspath(EXPORT_FOLDER)
    
    if not os.path.exists(abs_path):
        messagebox.showinfo("Thông báo", f"Thư mục '{EXPORT_FOLDER}' chưa được tạo.")
        os.makedirs(abs_path, exist_ok=True)
        return

    try:
        if os.name == 'nt':  # Đối với Windows
            os.startfile(abs_path)
        elif os.uname().sysname == 'Darwin':  # Đối với macOS
            subprocess.Popen(['open', abs_path])
        else: # Đối với Linux
            subprocess.Popen(['xdg-open', abs_path])
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")
    
#==============================SETTINGS ACCOUNT======================================
Username_HienTai = ""

def set_logged_in_user(username):
    """Hàm này CẦN được gọi sau khi đăng nhập thành công."""
    global Username_HienTai
    Username_HienTai = username

def get_current_username():
    """Trả về tên người dùng hiện tại, đảm bảo luôn có giá trị (vì đã đăng nhập)."""
    global Username_HienTai
    return Username_HienTai
def verify_user_password(username, submitted_password):
    """
    Truy vấn CSDL để lấy hash mật khẩu và xác minh bằng bcrypt.
    """   
    if not username or not submitted_password:
        return False
        
    conn = connect_to_db()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    password_match = False
    
    try:
        cursor.execute("SELECT MatKhauHash FROM NguoiDungHeThong WHERE TenDangNhap = ?", (username,))
        row = cursor.fetchone()
        
        if row:
            stored_hash = row[0] # Giả định đây là hash (string)
            
            submitted_bytes = submitted_password.encode('utf-8')
            
            if isinstance(stored_hash, str):
                stored_hash_bytes = stored_hash.encode('utf-8')
            else:
                stored_hash_bytes = stored_hash
                
            password_match = bcrypt.checkpw(submitted_bytes, stored_hash_bytes)
            
    except pyodbc.Error as e:
        print(f"Lỗi truy vấn xác minh mật khẩu: {e}")
    except Exception as e:
        print(f"Lỗi hệ thống khi xác minh: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
    return password_match

def handle_password_change(username, old_pw_entry, new_pw_entry, confirm_pw_entry):
    """Xác minh mật khẩu cũ và cập nhật mật khẩu mới (hash)."""
    old_password = old_pw_entry.get().strip()
    new_password = new_pw_entry.get().strip()
    confirm_password = confirm_pw_entry.get().strip()

    if not all([old_password, new_password, confirm_password]):
        messagebox.showerror("Lỗi", "Vui lòng điền đủ 3 trường mật khẩu.")
        return False
    
    if new_password != confirm_password:
        messagebox.showerror("Lỗi", "Mật khẩu Mới và Xác nhận Mật khẩu không khớp.")
        return False

    if not verify_user_password(username, old_password):
        messagebox.showerror("Lỗi Xác minh", "Mật khẩu CŨ không chính xác.")
        return False

    # Logic cập nhật (Sử dụng hash)
    conn = connect_to_db()
    if conn:
        try:
            hashed_new_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor = conn.cursor()
            sql_update = "UPDATE NguoiDungHeThong SET MatKhauHash = ? WHERE TenDangNhap = ?"
            cursor.execute(sql_update, (hashed_new_pw, username))
            conn.commit()
            
            messagebox.showinfo("Thành công", "Mật khẩu đã được cập nhật thành công!")
            
            # Xóa các trường sau khi thành công
            old_pw_entry.delete(0, 'end')
            new_pw_entry.delete(0, 'end')
            confirm_pw_entry.delete(0, 'end')
            return True
        except Exception as e:
            messagebox.showerror("Lỗi DB", f"Lỗi cập nhật mật khẩu: {e}")
        finally:
            conn.close()
    return False

def handle_email_change(new_email_entry, verification_entry):
    """
    Xác minh mật khẩu, kiểm tra định dạng email mới, và cập nhật Email trong DB.
    """
    # 1. Lấy dữ liệu và Username
    username = get_current_username() 
    new_email = new_email_entry.get().strip()
    current_password = verification_entry.get().strip()
    
    # --- RÀNG BUỘC (VALIDATION) ---
    if not all([username, new_email, current_password]):
        messagebox.showerror("Lỗi", "Vui lòng nhập Email mới và Mật khẩu hiện tại.")
        return False

    # Kiểm tra định dạng Email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
         messagebox.showerror("Lỗi", "Địa chỉ Email không hợp lệ.")
         return False

    # 2. XÁC MINH MẬT KHẨU CŨ 
    if not verify_user_password(username, current_password):
        messagebox.showerror("Lỗi Xác minh", "Mật khẩu hiện tại không chính xác. Không thể cập nhật.")
        return False # Hàm verify_user_password đã được sửa để trả về True/False

    # 3. CẬP NHẬT EMAIL
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Cập nhật cột Email trong bảng NguoiDungHeThong
            sql_update = "UPDATE NguoiDungHeThong SET Email = ? WHERE TenDangNhap = ?"
            cursor.execute(sql_update, (new_email, username))
            conn.commit()
            
            messagebox.showinfo("Thành công", f"Đã cập nhật Email thành công!")
            
            # 4. Dọn dẹp form và cập nhật giao diện
            verification_entry.delete(0, 'end')
            new_email_entry.delete(0, 'end')           
            
            return True
        except pyodbc.IntegrityError:
            messagebox.showerror("Lỗi DB", "Email này có thể đã được sử dụng bởi tài khoản khác.")
        except Exception as e:
            messagebox.showerror("Lỗi DB", f"Lỗi khi cập nhật Email: {e}")
        finally:
            if conn: conn.close()
    return False

def handle_name_change(new_name_entry, verification_entry):
    """
    Xác minh mật khẩu, kiểm tra Tên hiển thị mới, và cập nhật HoTenHienThi trong DB.
    """
    # 1. Lấy dữ liệu và Username
    username = get_current_username() 
    new_name = new_name_entry.get().strip()
    current_password = verification_entry.get().strip()
    
    # --- RÀNG BUỘC (VALIDATION) ---
    if not all([username, new_name, current_password]):
        messagebox.showerror("Lỗi", "Vui lòng nhập Tên hiển thị mới và Mật khẩu hiện tại.")
        return False

    # 2. XÁC MINH MẬT KHẨU CŨ (Bảo mật)
    if not verify_user_password(username, current_password):
        messagebox.showerror("Lỗi Xác minh", "Mật khẩu hiện tại không chính xác. Không thể cập nhật.")
        return False 

    # 3. CẬP NHẬT TÊN HIỂN THỊ
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Giả định cột là HoTenHienThi (hoặc cột tương ứng) trong bảng NguoiDungHeThong
            sql_update = "UPDATE NguoiDungHeThong SET HoTen = ? WHERE TenDangNhap = ?"
            cursor.execute(sql_update, (new_name, username))
            conn.commit()
            
            messagebox.showinfo("Thành công", f"Đã cập nhật Tên hiển thị thành công!")
            
            # 4. Dọn dẹp form và cập nhật giao diện
            verification_entry.delete(0, 'end')
            new_name_entry.delete(0, 'end')           
            
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi DB", f"Lỗi khi cập nhật Tên hiển thị: {e}")
        finally:
            if conn: conn.close()
    return False





def get_user_display_name():
        """Lấy Họ Tên/Tên hiển thị của người dùng đang đăng nhập từ DB."""
        username = get_current_username() 

        if not username or username == "LỖI: CHƯA ĐĂNG NHẬP":
            return "Bạn"
        
        conn = connect_to_db()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT HoTen FROM NguoiDungHeThong WHERE TenDangNhap = ?", (username,))
                row = cursor.fetchone()
                
                if row:
                    return row[0]            
            except Exception as e:
                print(f"Lỗi truy vấn tên hiển thị: {e}")
            finally:
                conn.close()
                
        return username

from .db_connect import connect_to_db
from tkinter import messagebox
import pyodbc
from gui import main
#======================================================================================
#===========================Hàm xử lý cho form quản lý sách============================
#======================================================================================
#1. Hàm thêm sách mới vào cơ sở dữ liệu
def add_book(book_widget):
    #Lấy dữ liệu từ form
    MaSach =  book_widget['MaSach'].get()
    TenSach = book_widget['TenSach'].get()
    TacGia =  book_widget['TacGia'].get()
    TheLoai = book_widget['TheLoai'].get()
    NhaXuatBan = book_widget['NhaXuatBan'].get()
    NamXuatBan = book_widget['NamXuatBan'].get()
    SoLuong = book_widget['SoLuong'].get()
    #Kiểm tra ràng buộc dữ liệu
    if not MaSach or not TenSach or not TacGia or not TheLoai or not NhaXuatBan or not NamXuatBan:
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin sách.")
        return
    if len(MaSach) != 7:
        messagebox.showerror("Lỗi", "Mã sách phải đúng 7 ký tự.")
        return
    if SoLuong:
        try:
            SoLuong = int(SoLuong)
            if SoLuong < 0:
                messagebox.showerror("Lỗi", "Số lượng tồn phải là số nguyên không âm.")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng tồn phải là số nguyên.")
            return
    else:
        SoLuong = 0  # Mặc định số lượng là 0 nếu không nhập
    #Kết nối đến cơ sở dữ liệu
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        #Chèn dữ liệu vào bảng Sách
        cursor.execute("""
            INSERT INTO Sach (MaSach, TenSach, TacGia, LoaiSach, NhaXuatBan, NamXuatBan, SoLuongTonKho)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (MaSach, TenSach, TacGia, TheLoai, NhaXuatBan, NamXuatBan, SoLuong))
        conn.commit()
        messagebox.showinfo("Thành công", "Thêm sách mới thành công!")
        for widget in book_widget.values():
            widget.delete(0, 'end')            
            load_book_data()  # Tải lại dữ liệu sách trong Treeview
            
    except pyodbc.IntegrityError:
        messagebox.showerror("Lỗi", "Mã sách đã tồn tại trong cơ sở dữ liệu.")    
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi thêm sách: {e}")
    finally:
        cursor.close()
        conn.close()
#2. Hàm cập nhật thông tin sách
def update_book(book_widget):
    #Lấy dữ liệu từ form
    MaSach =  book_widget['MaSach'].get()
    TenSach = book_widget['TenSach'].get()
    TacGia =  book_widget['TacGia'].get()
    TheLoai = book_widget['TheLoai'].get()
    NhaXuatBan = book_widget['NhaXuatBan'].get()
    NamXuatBan = book_widget['NamXuatBan'].get()
    SoLuong = book_widget['SoLuong'].get()
    #Kiểm tra ràng buộc dữ liệu
    if not MaSach:
        messagebox.showerror("Lỗi", "Vui lòng nhập Mã sách để cập nhật.")
        return
    if len(MaSach) != 7:
        messagebox.showerror("Lỗi", "Mã sách phải đúng 7 ký tự.")
        return
    if SoLuong:
        try:
            SoLuong = int(SoLuong)
            if SoLuong < 0:
                messagebox.showerror("Lỗi", "Số lượng tồn phải là số nguyên không âm.")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng tồn phải là số nguyên.")
            return
    else:
        SoLuong = 0  # Mặc định số lượng là 0 nếu không nhập
    #Kết nối đến cơ sở dữ liệu
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        #Cập nhật dữ liệu trong bảng Sách
        cursor.execute("""
            UPDATE Sach
            SET TenSach = ?, TacGia = ?, LoaiSach = ?, NhaXuatBan = ?, NamXuatBan = ?, SoLuongTonKho = ?
            WHERE MaSach = ?
        """, (TenSach, TacGia, TheLoai, NhaXuatBan, NamXuatBan, SoLuong, MaSach))
        if cursor.rowcount == 0:
            messagebox.showerror("Lỗi", "Mã sách không tồn tại trong cơ sở dữ liệu.")
        else:
            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật thông tin sách thành công!")
            for widget in book_widget.values():
                widget.delete(0, 'end')            
            load_book_data()  # Tải lại dữ liệu sách trong Treeview
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi cập nhật sách: {e}")
    finally:
        cursor.close()
        conn.close()
#3. Hàm xóa sách khỏi cơ sở dữ liệu
#4. Hàm tìm kiếm sách trong cơ sở dữ liệu
#5. Hiện thị danh sách sách từ cơ sở dữ liệu
book_entries = None
book_treeview = None
def register_book_entries(entries):
    global book_entries
    book_entries = entries
def register_book_treeview(treeview):
    global book_treeview
    book_treeview = treeview
def load_book_data():
    global book_treeview
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MaSach, TenSach, TacGia, LoaiSach, NhaXuatBan, NamXuatBan, SoLuongTonKho FROM Sach")
        rows = cursor.fetchall()
        # Xóa dữ liệu hiện tại trong Treeview
        for item in book_treeview.get_children():
            book_treeview.delete(item)
        # Thêm dữ liệu mới vào Treeview
        for row in rows:
            book_treeview.insert("", "end", values=list(row))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi tải danh sách sách: {e}")
    finally:
        cursor.close()
        conn.close()

def on_book_select(event):
    global book_entries
    selected_item = book_treeview.focus() # Lấy dòng đang được chọn
    if not selected_item:
        return   
    # Xóa dữ liệu cũ trong các ô Entry trước
    for key in book_entries:
         book_entries[key].delete(0, 'end')
    # Lấy dữ liệu từ dòng đã chọn
    book_data = book_treeview.item(selected_item)['values']   
    # Định nghĩa thứ tự các key khớp với thứ tự cột Treeview
    entry_keys = ['MaSach', 'TenSach', 'TacGia', 'TheLoai', 'NhaXuatBan', 'NamXuatBan', 'SoLuong']    
    # Điền dữ liệu vào các Entry tương ứng
    for key, value in zip(entry_keys, book_data):
        if key in book_entries:
            book_entries[key].insert(0, value) # Điền dữ liệu mới

    









    

    


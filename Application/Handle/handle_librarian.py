from .db_connect import connect_to_db 
from tkinter import messagebox
import pyodbc 
#===============================================================
#---1. Quản lý sách---
#===============================================================
#---I. Thêm sách---
# 1. Tạo một biến để lưu danh sách các Entry
_book_entries_ref = None
_book_treeview_ref = None

# 2. Tạo một hàm để nhận và lưu danh sách Entry từ UI
def register_book_entries(entries):
    global _book_entries_ref
    _book_entries_ref = entries
def register_book_treeview(treeview):
    global _book_treeview_ref
    _book_treeview_ref = treeview
# 3. Sử dụng biến này trong các hàm xử lý  
def add_book():
    global _book_entries_ref
    if _book_entries_ref is None:
        messagebox.showerror("Lỗi", "Không có dữ liệu để thêm sách.")
        return   
    conn = connect_to_db()
    if conn is None:
        messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
        return
    cursor = conn.cursor()
    try:
        ten_sach = _book_entries_ref[0].get()
        tac_gia = _book_entries_ref[1].get()
        the_loai = _book_entries_ref[2].get()
        so_luong = (_book_entries_ref[3].get())
        if not all([ten_sach, tac_gia, the_loai, so_luong]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin sách.")
            return
        try:
            so_luong_int = int(so_luong)
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là một số nguyên.")
            return
        if so_luong_int < 0:
            messagebox.showerror("Lỗi", "Số lượng không thể là số âm.")
            return
        cursor.execute("""
            INSERT INTO Sach (TenSach, TacGia, TheLoai, SoLuong)
            VALUES (?, ?, ?, ?)
        """, (ten_sach, tac_gia, the_loai, so_luong_int))
        conn.commit()
        messagebox.showinfo("Thành công", "Thêm sách thành công.")
        for entry in _book_entries_ref:
            entry.delete(0, 'end') 
            load_books_data()  # Cập nhật lại dữ liệu trong Treeview 
    except pyodbc.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm sách: {e}")
    finally:
        cursor.close()
        conn.close()
#---II. Sửa sách---
def edit_book():
    messagebox.showinfo("Chức năng chưa hoàn thiện", "Chức năng Sửa sách đang được phát triển.")
#---III. Xoá sách---
def delete_book():
    messagebox.showinfo("Chức năng chưa hoàn thiện", "Chức năng Xoá sách đang được phát triển.")
#---IV. Tìm kiếm sách---
def search_book():
    messagebox.showinfo("Chức năng chưa hoàn thiện", "Chức năng Tìm kiếm sách đang được phát triển.")
#--Lấy dữ liệu sách từ database để hiển thị lên Treeview--
def load_books_data():
    if _book_treeview_ref is None:
        messagebox.showerror("Lỗi", "Không có Treeview để hiển thị dữ liệu.")
        return
    for item in _book_treeview_ref.get_children():
        _book_treeview_ref.delete(item)
    conn = connect_to_db()
    if conn is None:
        messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
        return  
    cursor = conn.cursor()  
    try:
        cursor.execute("SELECT ID_Sach, TenSach, TacGia, TheLoai, SoLuong FROM Sach")
        rows = cursor.fetchall()
        for row in rows:
            _book_treeview_ref.insert("", "end", values=list(row))
    except pyodbc.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu sách: {e}")
    finally:
        cursor.close()
        conn.close()
def on_book_select(event_):
    selected_item = _book_treeview_ref.focus()
    if not selected_item:
        return
    book_data = _book_treeview_ref.item(selected_item, 'values')
    if _book_entries_ref is None or len(book_data) < 5:
        return
    for i in range(4):
        _book_entries_ref[i].delete(0, 'end')
        _book_entries_ref[i].insert(0, book_data[i+1])  # Bỏ qua ID_Sach
#===============================================================
     

    



   


    

from .db_connect import connect_to_db
from tkinter import messagebox
import pyodbc
import datetime
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
def delete_book(book_widget):
    MaSach = book_widget['MaSach'].get()
    if not MaSach:
        messagebox.showerror("Lỗi", "Vui lòng chọn sách để xóa.")
        return
    TenSach = book_widget['TenSach'].get()
    confirm = messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc chắn muốn xóa cuốn sách:\n\n"
                                  f"Mã sách: {MaSach}\n"
                                  f"Tên sách: {TenSach}\n\n"
                                  "Hành động này không thể hoàn tác.")
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Sach WHERE MaSach = ?", (MaSach,))
        if cursor.rowcount == 0:
            messagebox.showerror("Lỗi", "Mã sách không tồn tại trong cơ sở dữ liệu.")
        else:
            conn.commit()
            messagebox.showinfo("Thành công", "Xóa sách thành công!")
            for widget in book_widget.values():
                widget.delete(0, 'end')            
            load_book_data()  # Tải lại dữ liệu sách trong Treeview
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xóa sách: {e}")
    finally:
        cursor.close()
        conn.close()
#4. Hàm tìm kiếm sách trong cơ sở dữ liệu
def search_book(book_widget):
    global book_treeview
    tieuchuan = {
        'MaSach': book_widget['MaSach'].get(),
        'TenSach': book_widget['TenSach'].get(),
        'TacGia': book_widget['TacGia'].get(),
        'LoaiSach': book_widget['TheLoai'].get(),
        'NhaXuatBan': book_widget['NhaXuatBan'].get(),
        'NamXuatBan': book_widget['NamXuatBan'].get(),
    }

    searh_query = "SELECT MaSach, TenSach, TacGia, LoaiSach, NhaXuatBan, NamXuatBan, SoLuongTonKho FROM Sach WHERE 1=1"
    where_clauses = []
    params = []
    for key, value in tieuchuan.items():
        if value:
            where_clauses.append(f"{key} LIKE ?")
            params.append(f"%{value}%")
    if not where_clauses:
        load_book_data()
        messagebox.showinfo("Thông báo", "Đã tải lại toàn bộ danh sách sách.")
        return
    final_query = searh_query + " AND " + " AND ".join(where_clauses)
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(final_query, params)
        rows = cursor.fetchall()
        for item in book_treeview.get_children():
            book_treeview.delete(item)
        if not rows:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy sách phù hợp với tiêu chí.")
        else:
            for row in rows:
                book_treeview.insert("", "end", values=list(row))
            messagebox.showinfo("Kết quả tìm kiếm", f"Tìm thấy {len(rows)} cuốn sách phù hợp.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi tìm kiếm sách: {e}")
    finally:
        cursor.close()
        conn.close()   
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
#dọn textbox
def clear_book_entries(book_widget):
    for widget in book_widget.values():
        widget.delete(0, 'end') 
    if 'MaSach' in book_widget:
        book_widget['MaSach'].focus()           
#======================================================================================
#=========================Hàm xử lý cho form quản lý độc giả===========================
#======================================================================================
#1. Thêm độc giả
def add_reader(reader_widget):
    Madocgia = reader_widget['MaDocGia'].get()
    Hoten = reader_widget['HoTen'].get()
    Diachi = reader_widget['DiaChi'].get()
    Sodiendthoai = reader_widget['SoDienThoai'].get()
    Ngaysinh = reader_widget['NgaySinh'].get_date()
    #Kiểm tra ràng buộc dữ liệu
    if not Madocgia or not Hoten or not Diachi or not Sodiendthoai or not Ngaysinh:
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin độc giả.")
        return
    if len(Madocgia) != 6:
        messagebox.showerror("Lỗi", "Mã độc giả phải đúng 6 ký tự.")
        return
    if len(Sodiendthoai) != 10 or not Sodiendthoai.isdigit():
        messagebox.showerror("Lỗi", "Số điện thoại phải đúng 10 chữ số.")
        return
    #Kết nối đến cơ sở dữ liệu
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        #Chèn dữ liệu vào bảng Độc giả
        cursor.execute("""
            INSERT INTO DocGia (MaDocGia, HoTen, DiaChi, SoDienThoai, NgaySinh)
            VALUES (?, ?, ?, ?, ?)
        """, (Madocgia, Hoten, Diachi, Sodiendthoai, Ngaysinh))
        conn.commit()
        messagebox.showinfo("Thành công", "Thêm độc giả mới thành công!")
        for widget in reader_widget.values():
            widget.delete(0, 'end')            
            load_reader_data()  # Tải lại dữ liệu độc giả
            
    except pyodbc.IntegrityError:
        messagebox.showerror("Lỗi", "Mã độc giả đã tồn tại trong cơ sở dữ liệu.")    
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi thêm độc giả: {e}")
    finally:
        cursor.close()
        conn.close()
#2. Cập nhật thông tin độc giả
def update_reader(reader_widget):
    Madocgia = reader_widget['MaDocGia'].get()
    Hoten = reader_widget['HoTen'].get()
    Diachi = reader_widget['DiaChi'].get()
    Sodiendthoai = reader_widget['SoDienThoai'].get()
    Ngaysinh = reader_widget['NgaySinh'].get_date()
    #Kiểm tra ràng buộc dữ liệu
    if not Madocgia:
        messagebox.showerror("Lỗi", "Vui lòng nhập Mã độc giả để cập nhật.")
        return
    if len(Madocgia) != 6:
        messagebox.showerror("Lỗi", "Mã độc giả phải đúng 6 ký tự.")
        return
    if len(Sodiendthoai) != 10 or not Sodiendthoai.isdigit():
        messagebox.showerror("Lỗi", "Số điện thoại phải đúng 10 chữ số.")
        return
    #Kết nối đến cơ sở dữ liệu
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        #Cập nhật dữ liệu trong bảng Độc giả
        cursor.execute("""
            UPDATE DocGia
            SET HoTen = ?, DiaChi = ?, SoDienThoai = ?, NgaySinh = ?
            WHERE MaDocGia = ?
        """, (Hoten, Diachi, Sodiendthoai, Ngaysinh, Madocgia))
        if cursor.rowcount == 0:
            messagebox.showerror("Lỗi", "Mã độc giả không tồn tại trong cơ sở dữ liệu.")
        else:
            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật thông tin độc giả thành công!")
            for widget in reader_widget.values():
                widget.delete(0, 'end')            
            load_reader_data()  # Tải lại dữ liệu độc giả
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi cập nhật độc giả: {e}")
    finally:
        cursor.close()
        conn.close()
#3. Xóa độc giả khỏi cơ sở dữ liệu
def delete_reader(reader_widget):
    Madocgia = reader_widget['MaDocGia'].get()
    if not Madocgia:
        messagebox.showerror("Lỗi", "Vui lòng chọn độc giả để xóa.")
        return
    Hoten = reader_widget['HoTen'].get()
    confirm = messagebox.askyesno("Xác nhận xóa", 
                                  f"Bạn có chắc chắn muốn xóa độc giả:\n\n"
                                  f"Mã độc giả: {Madocgia}\n"
                                  f"Họ tên: {Hoten}\n\n"
                                  "Hành động này không thể hoàn tác.")
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM DocGia WHERE MaDocGia = ?", (Madocgia,))
        if cursor.rowcount == 0:
            messagebox.showerror("Lỗi", "Mã độc giả không tồn tại trong cơ sở dữ liệu.")
        else:
            conn.commit()
            messagebox.showinfo("Thành công", "Xóa độc giả thành công!")
            for widget in reader_widget.values():
                widget.delete(0, 'end')            
            load_reader_data()  # Tải lại dữ liệu độc giả
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xóa độc giả: {e}")
    finally:
        cursor.close()
        conn.close()
#4. Tìm kiếm
def search_reader(reader_widget):
    global reader_treeview
    tieuchuan = {
        'MaDocGia': reader_widget['MaDocGia'].get(),
        'HoTen': reader_widget['HoTen'].get(),
        'DiaChi': reader_widget['DiaChi'].get(),
        'SoDienThoai': reader_widget['SoDienThoai'].get(),
        #'NgaySinh': reader_widget['NgaySinh'].get_date(),
    }

    searh_query = "SELECT MaDocGia, HoTen, DiaChi, SoDienThoai, NgaySinh FROM DocGia WHERE 1=1"
    where_clauses = []
    params = []
    for key, value in tieuchuan.items():
        if value:
            where_clauses.append(f"{key} LIKE ?")
            params.append(f"%{value}%")
    if not where_clauses:
        load_reader_data()
        messagebox.showinfo("Thông báo", "Đã tải lại toàn bộ danh sách độc giả.")
        return
    final_query = searh_query + " AND " + " AND ".join(where_clauses)
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(final_query, params)
        rows = cursor.fetchall()
        for item in reader_treeview.get_children():
            reader_treeview.delete(item)
        if not rows:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy độc giả phù hợp với tiêu chí.")
        else:
            for row in rows:
                reader_treeview.insert("", "end", values=list(row))
            messagebox.showinfo("Kết quả tìm kiếm", f"Tìm thấy {len(rows)} độc giả phù hợp.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi tìm kiếm độc giả: {e}")
    finally:
        cursor.close()
        conn.close()
#5. Hiện thị danh sách độc giả từ cơ sở dữ liệu
reader_entries = None
reader_treeview = None
def register_reader_entries(entries):
    global reader_entries
    reader_entries = entries
def register_reader_treeview(treeview):
    global reader_treeview
    reader_treeview = treeview
def load_reader_data():
    global reader_treeview
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MaDocGia, HoTen, DiaChi, SoDienThoai, NgaySinh FROM DocGia")
        rows = cursor.fetchall()
        # Xóa dữ liệu hiện tại trong Treeview
        for item in reader_treeview.get_children():
            reader_treeview.delete(item)
        # Thêm dữ liệu mới vào Treeview
        for row in rows:
            # 1. Chuyển row (tuple) thành list để xử lý
            data_list = list(row)
            
            # 2. Xử lý cột Ngày sinh (vị trí 4)
            ngay_sinh = row[4] 
            if ngay_sinh:
                data_list[4] = ngay_sinh.strftime("%d/%m/%Y") 
                sdt = data_list[3]
            final_values = [str(v) for v in data_list]
            reader_treeview.insert("", "end", values = list(final_values))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi tải danh sách độc giả: {e}")
    finally:
        cursor.close()
        conn.close()
def on_reader_select(event):
    global reader_entries
    global reader_treeview
    
    selected_item = reader_treeview.focus()
    if not selected_item:
        return

    reader_data = reader_treeview.item(selected_item)['values']

    ma_doc_gia = str(reader_data[0]) 
    str_sdt = ""
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SoDienThoai FROM DocGia WHERE MaDocGia = ?", (ma_doc_gia,))
        row = cursor.fetchone()
        if row:
            str_sdt = str(row[0])
    except Exception as e:
        print(f"Lỗi khi truy vấn SĐT sạch: {e}") 
    finally:
        cursor.close()
        conn.close()

    for key, widget in reader_entries.items():
        if key != 'NgaySinh':
            widget.delete(0, 'end')

    entry_keys = ['MaDocGia', 'HoTen', 'DiaChi', 'SoDienThoai', 'NgaySinh']
    
    for key, value in zip(entry_keys, reader_data):
        if key in reader_entries:
            
            if key == 'SoDienThoai':
                reader_entries[key].insert(0, str_sdt)
            else:
                reader_entries[key].insert(0, str(value))

#dọn textbox
def clear_reader_entries(reader_widget):
    for key, widget in reader_widget.items():
        if key != 'NgaySinh':
            widget.delete(0, 'end')
        else:
            pass            
    if 'MaDocGia' in reader_widget:
        reader_widget['MaDocGia'].focus()
#======================================================================================
#=============================Hàm xử lý cho form mượn trả==============================
#======================================================================================
borrow_widgets = {}
def register_borrow_widgets(widgets_dict):
    global borrow_widgets
    borrow_widgets = widgets_dict
#Hàm tải Mã Độc Giả lên ComboBox
def load_reader_ids_to_combobox():
    try:
        if 'reader_combo' not in borrow_widgets:
            return
            
        conn = connect_to_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT MaDocGia FROM DocGia ORDER BY MaDocGia")
        rows = cursor.fetchall()
        
        reader_ids = [row[0] for row in rows]
        
        borrow_widgets['reader_combo'].configure(values=["Chọn mã độc giả"] + reader_ids)
        borrow_widgets['reader_combo'].set("Chọn mã độc giả")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        messagebox.showerror("LỖI CRASH (Độc Giả)", f"Không thể tải Mã Độc Giả: {e}")

#Hàm tải Mã Sách (còn) lên ComboBox 
def load_book_ids_to_combobox():
    try:
        if 'book_combo' not in borrow_widgets:
            return
            
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT MaSach FROM Sach WHERE SoLuongTonKho > 0 ORDER BY MaSach")
        rows = cursor.fetchall()
        
        book_ids = [row[0] for row in rows]
        
        borrow_widgets['book_combo'].configure(values=["Chọn mã sách"] + book_ids)
        borrow_widgets['book_combo'].set("Chọn mã sách")

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("LỖI CRASH (Sách)", f"Không thể tải Mã Sách: {e}")

#Hàm tự động điền Tên Độc Giả khi chọn Mã
def on_reader_id_select(selected_id):
    if 'reader_name' not in borrow_widgets:
        return
        
    name_entry = borrow_widgets['reader_name']

    # Mở khóa Entry để xóa/ghi
    name_entry.configure(state="normal")
    name_entry.delete(0, 'end')

    if selected_id == "Chọn mã độc giả":
        name_entry.configure(state="readonly")
        return

    # Lấy Tên từ DB
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT HoTen FROM DocGia WHERE MaDocGia = ?", (selected_id,))
        row = cursor.fetchone()
        if row:
            name_entry.insert(0, row[0]) # Điền tên
    except Exception as e:
         messagebox.showerror("Lỗi", f"Lỗi lấy tên độc giả: {e}")
    finally:
        cursor.close()
        conn.close()
    
    # Khóa Entry lại
    name_entry.configure(state="readonly")

#Hàm tự động điền Tên Sách khi chọn Mã
def on_book_id_select(selected_id):
    if 'book_name' not in borrow_widgets:
        return
        
    name_entry = borrow_widgets['book_name']

    name_entry.configure(state="normal")
    name_entry.delete(0, 'end')

    if selected_id == "Chọn mã sách":
        name_entry.configure(state="readonly")
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT TenSach FROM Sach WHERE MaSach = ?", (selected_id,))
        row = cursor.fetchone()
        if row:
            name_entry.insert(0, row[0])
    except Exception as e:
         messagebox.showerror("Lỗi", f"Lỗi lấy tên sách: {e}")
    finally:
        cursor.close()
        conn.close()
    
    name_entry.configure(state="readonly")





    


    










    

    


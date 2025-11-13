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
                data_list = list(row)
                ngay_sinh = row[4] 
                if ngay_sinh:
                    data_list[4] = ngay_sinh.strftime("%d/%m/%Y") 
                else:
                    data_list[4] = ""
                final_values = [str(v) for v in data_list]
                reader_treeview.insert("", "end", values=final_values)
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
# load phiếu
def load_borrow_list():
    # 1. Lấy Treeview
    phieu_muon_tree = borrow_widgets.get('phieu_muon_tree')
    if not phieu_muon_tree:
        print("Lỗi: 'phieu_muon_tree' chưa được đăng ký.")
        return

    # 2. Xóa dữ liệu cũ
    for item in phieu_muon_tree.get_children():
        phieu_muon_tree.delete(item)
        
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # 3. Câu SQL (Đã đơn giản hóa, không tính SUM)
        sql_query = """
            SELECT 
                pm.MaPhieuMuon, 
                pm.MaDocGia, 
                dg.HoTen, 
                pm.NgayMuon, 
                pm.NgayHenTra, 
                CASE 
                    WHEN pm.TrangThai = 0 THEN N'Đang Mượn'
                    WHEN pm.TrangThai = 1 THEN N'Đã Trả'
                    ELSE N'Không xác định'
                END AS TrangThaiChu
            FROM 
                PhieuMuon AS pm
            JOIN 
                DocGia AS dg ON pm.MaDocGia = dg.MaDocGia
            ORDER BY 
                pm.NgayMuon DESC
        """
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        
        # 4. Đổ dữ liệu vào Treeview
        for row in rows:
            data_list = list(row)
            
            # Định dạng 2 cột ngày tháng
            if data_list[3]: # NgayMuon
                data_list[3] = data_list[3].strftime("%d/%m/%Y")
            if data_list[4]: # NgayHenTra
                data_list[4] = data_list[4].strftime("%d/%m/%Y")
            
            phieu_muon_tree.insert("", "end", values=data_list)
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải danh sách phiếu mượn: {e}")
    finally:
        cursor.close()
        conn.close()

#======================================================================================
#==================== CÁC HÀM LOGIC CHO NÚT MƯỢN TRẢ SÁCH =============================
#======================================================================================

# --- HÀM CHO NÚT "HỦY/LÀM MỚI" ---
def clear_borrow_form():
    try:
        # 1. Lấy các widget
        cart_tree = borrow_widgets.get('cart_tree')
        reader_name_entry = borrow_widgets.get('reader_name')
        book_name_entry = borrow_widgets.get('book_name')

        # 2. Xóa các ô nhập liệu
        borrow_widgets.get('ma_phieu').delete(0, 'end')
        borrow_widgets.get('reader_combo').set("Chọn mã độc giả")
        
        reader_name_entry.configure(state="normal")
        reader_name_entry.delete(0, 'end')
        reader_name_entry.configure(state="readonly")
        
        borrow_widgets.get('book_combo').set("Chọn mã sách")
        book_name_entry.configure(state="normal")
        book_name_entry.delete(0, 'end')
        book_name_entry.configure(state="readonly")
        
        borrow_widgets.get('so_luong').delete(0, 'end')
        borrow_widgets.get('phi_phat').delete(0, 'end')
        borrow_widgets.get('tinh_trang').set("Tốt")
        
    except Exception as e:
        print(f"Lỗi khi xóa widget: {e}")

    # 3. Xóa tất cả item trong giỏ hàng (Treeview Chi Tiết)
    if cart_tree:
        for item in cart_tree.get_children():
            cart_tree.delete(item)
            
    # 4. Tải lại danh sách sách (vì số lượng tồn kho có thể đã thay đổi)
    load_book_ids_to_combobox()
    
    # 5. Tải lại danh sách phiếu mượn
    load_borrow_list() 

# --- HÀM CHO NÚT "THÊM SÁCH" (VÀO GIỎ HÀNG) ---
def add_book_to_cart():
    # 1. Lấy thông tin
    ma_sach = borrow_widgets.get('book_combo').get()
    ten_sach = borrow_widgets.get('book_name').get()
    so_luong_str = borrow_widgets.get('so_luong').get()
    cart_tree = borrow_widgets.get('cart_tree')
    
    # 2. Validate
    if ma_sach == "Chọn mã sách":
        messagebox.showerror("Lỗi", "Vui lòng chọn một cuốn sách.")
        return
    try:
        so_luong = int(so_luong_str)
        if so_luong <= 0: raise ValueError
    except ValueError:
        messagebox.showerror("Lỗi", "Số lượng phải là một số nguyên dương.")
        return

    # 3. Kiểm tra trùng lặp trong giỏ hàng
    for item_id in cart_tree.get_children():
        item_values = cart_tree.item(item_id, 'values')
        if item_values[0] == ma_sach:
            messagebox.showerror("Lỗi", f"Sách '{ma_sach}' đã có trong giỏ hàng.")
            return

    # 4. Kiểm tra Tồn Kho
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SoLuongTonKho FROM Sach WHERE MaSach = ?", (ma_sach,))
        row = cursor.fetchone()
        if not row or row[0] < so_luong:
            messagebox.showerror("Lỗi Tồn Kho", f"Không đủ số lượng. Sách '{ma_sach}' chỉ còn {row[0] if row else 0} cuốn.")
            return
    except Exception as e:
        messagebox.showerror("Lỗi DB", f"Lỗi kiểm tra tồn kho: {e}")
        return
    finally:
        cursor.close()
        conn.close()

    # 5. Thêm vào Treeview (Giỏ hàng)
    # (MaSach, TenSach, SoLuong, NgayTraTT, TinhTrang, PhiPhat)
    cart_values = (ma_sach, ten_sach, so_luong, "Chưa trả", "N/A", 0)
    cart_tree.insert("", "end", values=cart_values)
    
    # 6. Xóa ô nhập liệu
    borrow_widgets.get('book_combo').set("Chọn mã sách")
    borrow_widgets.get('book_name').configure(state="normal")
    borrow_widgets.get('book_name').delete(0, 'end')
    borrow_widgets.get('book_name').configure(state="readonly")
    borrow_widgets.get('so_luong').delete(0, 'end')

# --- HÀM CHO NÚT "XÓA SÁCH" (KHỎI GIỎ HÀNG) ---
def remove_book_from_cart():
    cart_tree = borrow_widgets.get('cart_tree')
    selected_item = cart_tree.focus() # Lấy dòng đang chọn
    
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn một cuốn sách trong bảng 'Chi Tiết Sách Mượn' để xóa.")
        return
        
    cart_tree.delete(selected_item)

# --- HÀM CHO NÚT "LƯU PHIẾU MƯỢN" ---
def save_borrow_ticket():
    # 1. Lấy thông tin Phiếu Mượn (Cột 0)
    ma_phieu = borrow_widgets.get('ma_phieu').get()
    ma_doc_gia = borrow_widgets.get('reader_combo').get()
    ngay_muon = borrow_widgets.get('ngay_muon').get_date()
    ngay_hen_tra = borrow_widgets.get('ngay_hen_tra').get_date()
    
    # 2. Lấy thông tin "Giỏ hàng" (Bảng Chi Tiết)
    cart_tree = borrow_widgets.get('cart_tree')
    cart_items_ids = cart_tree.get_children()
    
    book_list_to_save = []
    for item_id in cart_items_ids:
        values = cart_tree.item(item_id, 'values')
        ma_sach = values[0]
        so_luong = int(values[2])
        book_list_to_save.append((ma_sach, so_luong))

    # 3. Validate
    if not ma_phieu:
        messagebox.showerror("Lỗi", "Vui lòng nhập Mã Phiếu Mượn.")
        return
    if ma_doc_gia == "Chọn mã độc giả":
        messagebox.showerror("Lỗi", "Vui lòng chọn một Độc Giả.")
        return
    if not book_list_to_save:
        messagebox.showerror("Lỗi", "Giỏ hàng rỗng. Vui lòng thêm ít nhất 1 cuốn sách.")
        return
        
    # 4. Bắt đầu Transaction
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # SQL 1: Thêm Phiếu Mượn
        sql_phieumuon = """
            INSERT INTO PhieuMuon (MaPhieuMuon, MaDocGia, NgayMuon, NgayHenTra, TrangThai)
            VALUES (?, ?, ?, ?, 0)
        """ # 0 = Đang Mượn
        cursor.execute(sql_phieumuon, (ma_phieu, ma_doc_gia, ngay_muon, ngay_hen_tra))
        
        # SQL 2 & 3: Thêm Chi Tiết và Cập nhật Tồn Kho
        sql_chitiet = """
            INSERT INTO ChiTietPhieuMuon (MaPhieuMuon, MaSach, SoLuong, TinhTrang)
            VALUES (?, ?, ?, N'Tốt')
        """ # TinhTrang ban đầu là 'Tốt'
        sql_update_sach = """
            UPDATE Sach SET SoLuongTonKho = SoLuongTonKho - ? WHERE MaSach = ?
        """
        
        for ma_sach, so_luong in book_list_to_save:
            cursor.execute(sql_chitiet, (ma_phieu, ma_sach, so_luong))
            cursor.execute(sql_update_sach, (so_luong, ma_sach))

        # 5. Hoàn tất
        conn.commit()
        messagebox.showinfo("Thành công", f"Đã lưu thành công Phiếu Mượn {ma_phieu}!")
        
        # 6. Làm sạch form và tải lại
        clear_borrow_form() # Sẽ tự động gọi load_borrow_list()
        load_book_data()

    except pyodbc.IntegrityError as e:
        conn.rollback() 
        messagebox.showerror("Lỗi CSDL", f"Lỗi: Mã Phiếu Mượn '{ma_phieu}' đã tồn tại.\n{e}")
    except Exception as e:
        conn.rollback() 
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi lưu phiếu mượn: {e}")
    finally:
        cursor.close()
        conn.close()

# --- HÀM TẢI CHI TIẾT KHI CLICK PHIẾU MƯỢN ---
def load_chi_tiet_phieu(ma_phieu):
    cart_tree = borrow_widgets.get('cart_tree')
    
    # Xóa giỏ hàng cũ
    for item in cart_tree.get_children():
        cart_tree.delete(item)

    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Lấy chi tiết của phiếu này
        sql_query = """
            SELECT 
                ct.MaSach, 
                s.TenSach, 
                ct.SoLuong,
                ct.NgayTraThucTe,
                ct.TinhTrang,
                ct.PhiPhat
            FROM 
                ChiTietPhieuMuon AS ct
            JOIN 
                Sach AS s ON ct.MaSach = s.MaSach
            WHERE 
                ct.MaPhieuMuon = ?
        """
        cursor.execute(sql_query, (ma_phieu,))
        rows = cursor.fetchall()
        
        for row in rows:
            data_list = list(row)
            
            # Format Ngày Trả
            if data_list[3]: # NgayTraThucTe
                data_list[3] = data_list[3].strftime("%d/%m/%Y")
            else:
                data_list[3] = "Chưa trả"
                
            # Format Phí Phạt
            if data_list[5] is None:
                data_list[5] = 0
                
            cart_tree.insert("", "end", values=data_list)
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải chi tiết phiếu: {e}")
    finally:
        cursor.close()
        conn.close()

# --- HÀM XỬ LÝ CLICK BẢNG "DANH SÁCH PHIẾU MƯỢN" ---
def on_phieu_muon_select(event):
    phieu_tree = borrow_widgets.get('phieu_muon_tree')
    selected_item = phieu_tree.focus()
    if not selected_item:
        return
        
    # Lấy dữ liệu từ dòng được chọn
    # (MaPhiếu, MaĐG, TênĐG, NgayMượn, HạnTrả, TrạngThái)
    data = phieu_tree.item(selected_item, 'values')
    
    ma_phieu = data[0]
    ma_doc_gia = data[1]
    ngay_muon_str = data[3]
    ngay_hen_tra_str = data[4]

    # 1. Điền thông tin vào Cột 0
    borrow_widgets.get('ma_phieu').delete(0, 'end')
    borrow_widgets.get('ma_phieu').insert(0, ma_phieu)
    borrow_widgets.get('reader_combo').set(ma_doc_gia)
    
    borrow_widgets.get('reader_name').configure(state="normal")
    borrow_widgets.get('reader_name').delete(0, 'end')
    borrow_widgets.get('reader_name').insert(0, data[2]) # Tên ĐG
    borrow_widgets.get('reader_name').configure(state="readonly")
    
    try:
        ngay_muon_obj = datetime.datetime.strptime(ngay_muon_str, "%d/%m/%Y").date()
        borrow_widgets.get('ngay_muon').set_date(ngay_muon_obj)
    except ValueError:
        borrow_widgets.get('ngay_muon').delete(0, 'end')
        borrow_widgets.get('ngay_muon').insert(0, ngay_muon_str)
        
    try:
        ngay_hen_tra_obj = datetime.datetime.strptime(ngay_hen_tra_str, "%d/%m/%Y").date()
        borrow_widgets.get('ngay_hen_tra').set_date(ngay_hen_tra_obj)
    except ValueError:
        borrow_widgets.get('ngay_hen_tra').delete(0, 'end')
        borrow_widgets.get('ngay_hen_tra').insert(0, ngay_hen_tra_str)

    # 2. Tải chi tiết sách vào Bảng 2
    load_chi_tiet_phieu(ma_phieu)
    
    # 3. Chuyển Tab sang "Trả Sách"
    borrow_widgets.get('tab_view').set("Xử Lý Trả Sách")


# --- HÀM XỬ LÝ CLICK BẢNG "CHI TIẾT" (GIỎ HÀNG) ---
def on_chi_tiet_select(event):
    cart_tree = borrow_widgets.get('cart_tree')
    selected_item = cart_tree.focus()
    if not selected_item:
        return
        
    # (MaSach, TenSach, SL, NgayTraTT, TinhTrang, PhiPhat)
    data = cart_tree.item(selected_item, 'values')
    
    ngay_tra_str = data[3]
    tinh_trang = data[4]
    phi_phat = data[5]

    # 1. Điền thông tin vào Tab "Xử Lý Trả Sách"
    if ngay_tra_str != "Chưa trả":
        try:
            ngay_tra_obj = datetime.datetime.strptime(ngay_tra_str, "%d/%m/%Y").date()
            borrow_widgets.get('ngay_tra_tt').set_date(ngay_tra_obj)
        except ValueError:
            borrow_widgets.get('ngay_tra_tt').delete(0, 'end')
    else:
        borrow_widgets.get('ngay_tra_tt').set_date(datetime.date.today()) # Đặt ngày hôm nay

    borrow_widgets.get('tinh_trang').set(tinh_trang if tinh_trang != "N/A" else "Tốt")
    
    borrow_widgets.get('phi_phat').delete(0, 'end')
    borrow_widgets.get('phi_phat').insert(0, phi_phat)
    
    # 2. Chuyển Tab
    borrow_widgets.get('tab_view').set("Xử Lý Trả Sách")

# --- HÀM CHO NÚT "CẬP NHẬT TRẢ" ---
def update_book_return():
    # 1. Lấy thông tin
    ma_phieu = borrow_widgets.get('ma_phieu').get()
    cart_tree = borrow_widgets.get('cart_tree')
    selected_item = cart_tree.focus()
    
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn một cuốn sách từ bảng 'Chi Tiết Sách Mượn' để cập nhật trả.")
        return
        
    # 2. Lấy thông tin sách cần trả
    selected_book_data = cart_tree.item(selected_item, 'values')
    ma_sach = selected_book_data[0]
    so_luong_tra = int(selected_book_data[2])
    ngay_tra_cu = selected_book_data[3]

    if ngay_tra_cu != "Chưa trả":
        messagebox.showinfo("Thông báo", f"Sách '{ma_sach}' đã được trả vào ngày {ngay_tra_cu}.")
        return

    # 3. Lấy thông tin từ Tab "Trả Sách"
    ngay_tra_moi = borrow_widgets.get('ngay_tra_tt').get_date()
    tinh_trang_moi = borrow_widgets.get('tinh_trang').get()
    phi_phat_str = borrow_widgets.get('phi_phat').get()
    
    try:
        phi_phat = int(phi_phat_str) if phi_phat_str else 0
    except ValueError:
        messagebox.showerror("Lỗi", "Phí phạt phải là một con số.")
        return
        
    # 4. Transaction
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # SQL 1: Cập nhật Chi Tiết
        sql_update_chitiet = """
            UPDATE ChiTietPhieuMuon
            SET NgayTraThucTe = ?, TinhTrang = ?, PhiPhat = ?
            WHERE MaPhieuMuon = ? AND MaSach = ?
        """
        cursor.execute(sql_update_chitiet, (ngay_tra_moi, tinh_trang_moi, phi_phat, ma_phieu, ma_sach))
        
        # SQL 2: Cập nhật Tồn Kho (Chỉ cộng lại nếu sách 'Tốt' hoặc 'Hư hỏng nhẹ')
        if tinh_trang_moi in ["Tốt", "Hư hỏng nhẹ"]:
            sql_update_sach = "UPDATE Sach SET SoLuongTonKho = SoLuongTonKho + ? WHERE MaSach = ?"
            cursor.execute(sql_update_sach, (so_luong_tra, ma_sach))
            
        conn.commit()
        
        # 5. Kiểm tra xem phiếu đã trả hết chưa
        cursor.execute("""
            SELECT COUNT(*) 
            FROM ChiTietPhieuMuon 
            WHERE MaPhieuMuon = ? AND NgayTraThucTe IS NULL
        """, (ma_phieu,))
        sach_con_lai = cursor.fetchone()[0]
        
        if sach_con_lai == 0:
            # SQL 3: Cập nhật Trạng Thái Phiếu Mượn
            cursor.execute("UPDATE PhieuMuon SET TrangThai = 1 WHERE MaPhieuMuon = ?", (ma_phieu,)) # 1 = Đã Trả
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã trả sách '{ma_sach}'.\nPhiếu '{ma_phieu}' đã được trả đầy đủ!")
        else:
            messagebox.showinfo("Thành công", f"Đã trả sách '{ma_sach}'.\nPhiếu '{ma_phieu}' còn {sach_con_lai} cuốn chưa trả.")
            
        # 6. Tải lại cả hai bảng
        load_borrow_list()
        load_chi_tiet_phieu(ma_phieu)
        load_book_ids_to_combobox() # Tải lại ComboBox Sách
        load_book_data()

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi cập nhật trả sách: {e}")
    finally:
        cursor.close()
        conn.close()

# --- HÀM CHO NÚT "TRA CỨU PHIẾU" ---
def search_borrow_ticket():
    # 1. Lấy Treeview
    phieu_muon_tree = borrow_widgets.get('phieu_muon_tree')
    if not phieu_muon_tree: return

    # 2. Xóa dữ liệu cũ
    for item in phieu_muon_tree.get_children():
        phieu_muon_tree.delete(item)
        
    # 3. Lấy tiêu chí
    ma_phieu = borrow_widgets.get('ma_phieu').get()
    ma_doc_gia = borrow_widgets.get('reader_combo').get()
    
    # 4. Xây dựng câu SQL
    base_sql = """
        SELECT 
            pm.MaPhieuMuon, pm.MaDocGia, dg.HoTen, 
            pm.NgayMuon, pm.NgayHenTra, 
            CASE 
                WHEN pm.TrangThai = 0 THEN 'Đang Mượn'
                WHEN pm.TrangThai = 1 THEN 'Đã Trả'
                ELSE 'Không xác định'
            END AS TrangThaiChu
        FROM PhieuMuon AS pm
        JOIN DocGia AS dg ON pm.MaDocGia = dg.MaDocGia
    """
    
    where_clauses = []
    params = []
    
    if ma_phieu:
        where_clauses.append("pm.MaPhieuMuon LIKE ?")
        params.append(f"%{ma_phieu}%")
        
    if ma_doc_gia != "Chọn mã độc giả":
        where_clauses.append("pm.MaDocGia = ?")
        params.append(ma_doc_gia)
        
    if not where_clauses:
        load_borrow_list()
        messagebox.showinfo("Thông báo", "Đã tải lại toàn bộ danh sách phiếu.")
        return
        
    final_sql = base_sql + " WHERE " + " AND ".join(where_clauses) + " ORDER BY pm.NgayMuon DESC"

    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(final_sql, params)
        rows = cursor.fetchall()
        
        if not rows:
            messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nào phù hợp.")
            return

        for row in rows:
            data_list = list(row)
            if data_list[3]: data_list[3] = data_list[3].strftime("%d/%m/%Y")
            if data_list[4]: data_list[4] = data_list[4].strftime("%d/%m/%Y")
            phieu_muon_tree.insert("", "end", values=data_list)
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tìm kiếm phiếu mượn: {e}")
    finally:
        cursor.close()
        conn.close()





    


    










    

    


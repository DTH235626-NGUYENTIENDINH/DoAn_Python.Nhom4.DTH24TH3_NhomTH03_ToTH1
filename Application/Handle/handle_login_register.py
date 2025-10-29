from .db_connect import connect_to_db
from tkinter import messagebox
from Application.UI import librarian_ui, readers_ui
import pyodbc
import bcrypt


def handle_register(txtHoTen, txtUsername, txtSDT, txtPassword, txtLibarianCode):

    """
    Xử lý logic đăng ký người dùng, lấy dữ liệu từ các đối tượng Entry Tkinter
    và lưu vào CSDL.
    """
    ho_ten = txtHoTen.get()
    username = txtUsername.get()
    sdt = txtSDT.get()
    password = txtPassword.get()
    role = txtLibarianCode.get()
    
    # 1. Kiểm tra dữ liệu rỗng
    if not all([ho_ten, username, sdt, password]):
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
        return

    # GỌI HÀM KẾT NỐI CSDL
    conn = connect_to_db() 
    if conn is None:
        # Hàm connect_to_db() của bạn đã in lỗi, nên chỉ cần thoát
        return
    
    try:
        cursor = conn.cursor()

        # 2. Kiểm tra Tên đăng nhập đã tồn tại (SỬ DỤNG TÊN CỘT CHÍNH XÁC: _Username)
        cursor.execute("SELECT ID_user FROM NGUOIDUNG WHERE _Username = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.")
            return


        # 3. Mã hóa mật khẩu
        password_temp = password.encode('utf-8')
        hash_password  = bcrypt.hashpw(password_temp, bcrypt.gensalt())
        hash_password_temp = hash_password.decode('utf-8')



        # 4. Thêm người dùng mới (Mặc định User_Role là 'User')

        # 3. Thêm người dùng mới
        if role == "AGU_LIB":
            user_role = 1  # Thủ thư
        else:
            user_role = 0  # Đọc giả

        insert_query = """
        INSERT INTO NGUOIDUNG (HoTen, _Username, _Password, SDT, User_Role)
        VALUES (?, ?, ?, ?, ?) 
        """

        cursor.execute(insert_query, (ho_ten, username, hash_password_temp, sdt))

        cursor.execute(insert_query, (ho_ten, username, password, sdt, user_role))

        conn.commit()

        messagebox.showinfo("Thành công", "Đăng ký thành công!")
        
        # Xóa các trường nhập liệu
        txtHoTen.delete(0, 'end')
        txtUsername.delete(0, 'end')
        txtSDT.delete(0, 'end')
        txtPassword.delete(0, 'end')
        
    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi CSDL", f"Lỗi khi lưu dữ liệu:\n{ex}")
    finally:
        if conn:
            conn.close()


def toggle_password_visibility(checked_state, txtPassword):
    """Chuyển đổi thuộc tính show của ô nhập mật khẩu."""
    if checked_state.get() == 1:
        txtPassword.config(show="") 
    else:
        txtPassword.config(show="*")

#Xử lý đăng nhập
def handle_login(txtUsername, txtPassword):
    """
    Xử lý logic đăng nhập người dùng, lấy dữ liệu từ các đối tượng Entry Tkinter
    và kiểm tra trong CSDL.
    """
    username = txtUsername.get()
    password = txtPassword.get()
    
    # 1. Kiểm tra dữ liệu rỗng
    if not all([username, password]):
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
        return

    # GỌI HÀM KẾT NỐI CSDL
    conn = connect_to_db() 
    if conn is None:
        # Hàm connect_to_db() của bạn đã in lỗi, nên chỉ cần thoát
        return
    
    try:
        cursor = conn.cursor()

        # 2. Kiểm tra Tên đăng nhập và Mật khẩu (SỬ DỤNG TÊN CỘT CHÍNH XÁC: _Username, _Password)
        cursor.execute("SELECT ID_user, HoTen, User_Role FROM NGUOIDUNG WHERE _Username = ? AND _Password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            user_id, ho_ten, tempuser_role = user
            if tempuser_role == 1:
                user_role = 'Thủ thư'
            else:
                user_role = 'Đọc giả'
            messagebox.showinfo("Thành công", f"Đăng nhập thành công!\nChào mừng {ho_ten} (ID: {user_id}, Role: {user_role})")
            # Ở đây bạn có thể chuyển đến giao diện chính của ứng dụng
            if tempuser_role == 1:
                librarian_ui.librarian_ui()
            else:
                readers_ui.reader_ui()

        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")
            return
               
    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi CSDL", f"Lỗi khi truy vấn dữ liệu:\n{ex}")
    finally:
        if conn:
            conn.close()

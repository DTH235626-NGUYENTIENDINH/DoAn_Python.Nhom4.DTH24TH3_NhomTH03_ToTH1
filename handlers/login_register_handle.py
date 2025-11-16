from .db_connect import connect_to_db
import pyodbc
import bcrypt
import re
from handlers.persistense_manager_2 import *
def handle_register(full_name, email, username, password, confirm_password):
    """
    Xử lý đăng ký (TenDangNhap, MatKhauHash, HoTen)
    """

    if not all([full_name, email, username, password, confirm_password]):
        return False, "Vui lòng điền đầy đủ tất cả các trường."
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, "Định dạng email không hợp lệ."
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        return False, "Tên đăng nhập chỉ được chứa chữ cái và số."
    if password != confirm_password:
        return False, "Mật khẩu và xác nhận mật khẩu không khớp."
    if len(password) < 3:
        return False, "Mật khẩu phải có ít nhất 3 ký tự."

    conn = None
    cursor = None

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM NguoiDungHeThong WHERE TenDangNhap = ? OR Email = ?", (username, email))
        if cursor.fetchone()[0] > 0:
            return False, "Tên đăng nhập hoặc email đã tồn tại."

        # Mã hóa mật khẩu
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO NguoiDungHeThong (TenDangNhap, MatKhauHash, Email, HoTen) VALUES (?, ?, ?, ?)",
            (username, hashed_password, email, full_name)
        )
        conn.commit()
        return True, "Đăng ký thành công!"
    except Exception as e:
        print(f"Lỗi SQL khi đăng ký: {str(e)}") 
        return False, f"Lỗi khi kết nối đến cơ sở dữ liệu: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def handle_login(username, password):
    """
    Xử lý đăng nhập - ĐÃ SỬA để khớp với tên cột CSDL (TenDangNhap, MatKhauHash, HoTen)
    """
    
    if not all([username, password]):
        return False, "Vui lòng điền đầy đủ tên đăng nhập và mật khẩu."
    
    conn = None
    cursor = None
    
    try: 
        conn = connect_to_db()
        if conn is None:
            return False, "Không thể kết nối đến CSDL."
            
        cursor = conn.cursor()
        
        # Lấy thông tin người dùng BẰNG TÊN CỘT ĐÚNG
        sql_query = "SELECT MatKhauHash, HoTen FROM NguoiDungHeThong WHERE TenDangNhap = ?"
        cursor.execute(sql_query, (username,))
        
        user_data = cursor.fetchone() 

        if user_data:
            # user_data[0] là MatKhauHash
            # user_data[1] là HoTen
            hashed_password_from_db = user_data[0]
            full_name = user_data[1]
            
            # Dùng bcrypt.checkpw để so sánh
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
                # ĐĂNG NHẬP THÀNH CÔNG
                set_logged_in_user(username)
                return True, f"Chào mừng {full_name}!"
            else:
                # Sai mật khẩu
                return False, "Tên đăng nhập hoặc mật khẩu không đúng."
        else:
            # Không tìm thấy username
            return False, "Tên đăng nhập hoặc mật khẩu không đúng."
    
    except pyodbc.Error as e:
        print(f"Lỗi SQL khi đăng nhập: {str(e)}")
        return False, "Lỗi khi truy vấn cơ sở dữ liệu."
    except Exception as e:
        print(f"Lỗi không xác định khi đăng nhập: {str(e)}")
        return False, "Đã xảy ra lỗi không mong muốn."

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
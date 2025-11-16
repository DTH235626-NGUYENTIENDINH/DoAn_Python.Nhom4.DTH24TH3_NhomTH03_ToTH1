import customtkinter as ctk
from PIL import Image
import os
import pyodbc
import re
import bcrypt
from handlers.login_register_handle import handle_register, handle_login

class App(ctk.CTk):

    # Kích thước cửa sổ chính
    WINDOW_WIDTH = 1000
    # Tăng chiều cao để chứa khung đăng ký 480px và lề
    WINDOW_HEIGHT = 600 
    # Kích thước cố định cho khung ở giữa
    FRAME_WIDTH = 350
    FRAME_HEIGHT_REGISTER = 480 
    FRAME_HEIGHT_LOGIN = 380    

    def __init__(self,on_login_success_callback):
        super().__init__()
        self.title("Giao diện với ảnh nền")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False) 

        self.on_login_success = on_login_success_callback

        # === 1. Ảnh nền cho TOÀN BỘ CỬA SỔ ===
        image_path = os.path.join("Picture", "Background1.jpg") 
        self.bg_label = self._create_window_background(image_path)
        
        # === 2. Label thông báo  ===
        self.message_label = ctk.CTkLabel(self, text="", text_color="red", 
                                          font=ctk.CTkFont(size=14, weight="bold"))
        self.message_label.place(relx=0.5, rely=0.05, anchor="center")
        # === 3. Tạo frame con ===
        self.login_frame = ctk.CTkFrame(self, corner_radius=20, 
                                        width=self.FRAME_WIDTH, 
                                        height=self.FRAME_HEIGHT_LOGIN,
                                        fg_color=("#F0F0F0", "gray15"), 
                                        border_width=2,
                                        border_color="gray") 
        
        self.register_frame = ctk.CTkFrame(self, corner_radius=20, 
                                           width=self.FRAME_WIDTH, 
                                           height=self.FRAME_HEIGHT_REGISTER,
                                           fg_color=("#F0F0F0", "gray15"),
                                           border_width=2,
                                           border_color="gray")

        # === 4. Thiết lập giao diện cho từng frame ===
        self.setup_login_ui()
        self.setup_register_ui()

        # === 5. Hiển thị frame Đăng nhập ban đầu ===
        self.show_login_frame()
        
    def _create_window_background(self, image_path):
        """Tạo và đặt ảnh nền cho cửa sổ chính (lớp dưới cùng)"""
        if not os.path.exists(image_path):
            print(f"Lỗi: Không tìm thấy ảnh nền cửa sổ '{image_path}'")
            bg_label = ctk.CTkLabel(self, text="Background missing!", fg_color="gray20") 
        else:
            try:
                bg_image_pil = Image.open(image_path)
                bg_image = ctk.CTkImage(bg_image_pil, 
                                         size=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
                bg_label = ctk.CTkLabel(self, image=bg_image, text="")
            except Exception as e:
                print(f"Lỗi khi tải ảnh nền cửa sổ: {e}")
                bg_label = ctk.CTkLabel(self, text="Error loading background!", fg_color="gray20")
        
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        return bg_label
    
    def show_message(self, message, is_error=True):
        """Hiển thị thông báo (thành công hoặc lỗi) ở phía trên cửa sổ."""
        self.message_label.configure(text=message, 
                                     text_color="red" if is_error else "green")
        # Thiết lập để xóa thông báo sau 5 giây
        self.after(5000, lambda: self.message_label.configure(text=""))



    def setup_login_ui(self):
        """Thiết lập giao diện Đăng nhập (Đã điều chỉnh màu sắc và lề)"""
        frame = self.login_frame
        
        # --- Các Widget  ---

        label = ctk.CTkLabel(frame, text="Đăng nhập", 
                             font=ctk.CTkFont(size=26, weight="bold"),
                             text_color=("#1A1A1A", "white")) 
        label.pack(pady=(40, 25), padx=30) 

        # Kiểu dáng chung cho ô nhập liệu
        entry_kwargs = {
            "width": 250, 
            "height": 36, 
            "border_color": "#2196F3",         
            "fg_color": ("white", "gray25"),   
            "text_color": ("#1A1A1A", "white"),
            "placeholder_text_color": ("gray60", "gray50"), 
        }

        self.login_username_entry = ctk.CTkEntry(frame, 
                                                 placeholder_text="Tên đăng nhập", 
                                                 **entry_kwargs)
        self.login_username_entry.pack(pady=10, padx=30)

        self.login_password_entry = ctk.CTkEntry(frame, 
                                                 placeholder_text="Mật khẩu", 
                                                 show="*", 
                                                 **entry_kwargs)
        self.login_password_entry.pack(pady=10, padx=30)

        # NÚT ĐĂNG NHẬP
        login_button = ctk.CTkButton(frame, text="Đăng nhập", 
                                     width=250, 
                                     height=40, 
                                     corner_radius=10,
                                     fg_color="#2196F3",    
                                     hover_color="#64B5F6",
                                     command=self.handle_login) 
        login_button.pack(pady=(25, 15), padx=30) 

        # Nút chuyển đổi
        switch_button = ctk.CTkButton(
            frame,
            text="Chưa có tài khoản? Đăng ký",
            fg_color="transparent", 
            hover_color="gray", 
            text_color=("#1A1A1A", "white"), 
            font=ctk.CTkFont(weight="bold", underline=True, size=13),
            command=self.show_register_frame
        )
        switch_button.pack(pady=(10, 30), padx=30)

    def setup_register_ui(self):
        """Thiết lập giao diện Đăng ký (Đã điều chỉnh màu sắc và lề)"""
        frame = self.register_frame

        # --- Các Widget ---
        label = ctk.CTkLabel(frame, text="Đăng ký", 
                             font=ctk.CTkFont(size=26, weight="bold"),
                             text_color=("#1A1A1A", "white")) 
        label.pack(pady=(20, 10), padx=30) 

        # Kiểu dáng chung cho ô nhập liệu
        entry_kwargs = {
            "width": 250, 
            "height": 36, 
            "border_color": "#2196F3",         
            "fg_color": ("white", "gray25"),   
            "text_color": ("#1A1A1A", "white"),
            "placeholder_text_color": ("gray60", "gray50"),
        }

        # Điều chỉnh lề dọc (pady) để nhét vừa đủ 5 ô nhập liệu
        self.reg_fullname_entry = ctk.CTkEntry(frame, placeholder_text="Họ và tên", **entry_kwargs)
        self.reg_fullname_entry.pack(pady=5, padx=30)

        self.reg_email_entry = ctk.CTkEntry(frame, placeholder_text="Gmail", **entry_kwargs)
        self.reg_email_entry.pack(pady=5, padx=30)

        self.reg_username_entry = ctk.CTkEntry(frame, placeholder_text="Tên đăng nhập", **entry_kwargs)
        self.reg_username_entry.pack(pady=5, padx=30)

        self.reg_password_entry = ctk.CTkEntry(frame, placeholder_text="Mật khẩu", show="*", **entry_kwargs)
        self.reg_password_entry.pack(pady=5, padx=30)

        self.reg_confirm_entry = ctk.CTkEntry(frame, placeholder_text="Xác nhận mật khẩu", show="*", **entry_kwargs)
        self.reg_confirm_entry.pack(pady=5, padx=30)

        self.reg_show_pass_var = ctk.BooleanVar(value=False)

        show_pass_check = ctk.CTkCheckBox(
            frame,
            text="Hiện mật khẩu",
            variable=self.reg_show_pass_var,
            onvalue=True,
            offvalue=False,
            command=self.toggle_password_visibility, # Gọi phương thức CỦA CLASS
            text_color=("#1A1A1A", "white")
        )

        show_pass_check.pack(pady=(10, 5), padx=40, anchor="w") 

        # NÚT ĐĂNG KÝ 
        register_button = ctk.CTkButton(frame, text="Đăng ký", 
                                        width=250, 
                                        height=40,
                                        corner_radius=10,
                                        fg_color="#2196F3",    
                                        hover_color="#64B5F6", 
                                        command=self.handle_register)                                       
        register_button.pack(pady=(15, 10), padx=30) 

        # Nút chuyển đổi
        switch_button = ctk.CTkButton(
            frame,
            text="Đã có tài khoản? Đăng nhập",
            fg_color="transparent", 
            hover_color="gray", 
            text_color=("#1A1A1A", "white"),
            font=ctk.CTkFont(weight="bold", underline=True, size=13),
            command=self.show_login_frame
        )
        switch_button.pack(pady=(10, 20), padx=30) 


    def show_login_frame(self):
        """Hiển thị giao diện đăng nhập"""
        self.register_frame.place_forget() 
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center") 
        self.title("Quản lý sách - Đăng nhập")
        self.show_message("", is_error=True) 

    def show_register_frame(self):
        """Hiển thị giao diện đăng ký"""
        self.login_frame.place_forget() 
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center") 
        self.title("Quản lý sách - Đăng ký")
        self.show_message("", is_error=True) 

    def handle_register(self):
        """Lấy dữ liệu từ UI và gọi logic đăng ký DB."""
        full_name = self.reg_fullname_entry.get()
        email = self.reg_email_entry.get()
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_entry.get()

        # Gọi hàm từ db_logic.py
        success, message = handle_register(full_name, email, username, password, confirm_password)

        if success:
            self.show_message(message, is_error=False)
            # Xóa sạch các trường nhập liệu
            self.reg_fullname_entry.delete(0, 'end')
            self.reg_email_entry.delete(0, 'end')
            self.reg_username_entry.delete(0, 'end')
            self.reg_password_entry.delete(0, 'end')
            self.reg_confirm_entry.delete(0, 'end')
            # Chuyển về màn hình đăng nhập
            self.after(2000, self.show_login_frame) 
        else:
            self.show_message(message, is_error=True)

    def handle_login(self):
        """Lấy dữ liệu từ UI và gọi logic đăng nhập DB."""
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

       
        success, message = handle_login(username, password)

        if success:
            if self.on_login_success:
                self.on_login_success(message)
            self.destroy()  # Đóng cửa sổ đăng nhập
        else:
            self.show_message(message, is_error=True)

    def toggle_password_visibility(self):

        if self.reg_show_pass_var.get():  # Trả về True nếu checkbox được tick
            # Nếu được tick, đặt show="" để hiển thị văn bản
            self.reg_password_entry.configure(show="")
            self.reg_confirm_entry.configure(show="")
        else:  # Trả về False nếu checkbox không được tick
            # Nếu không tick, đặt show="*" để ẩn văn bản
            self.reg_password_entry.configure(show="*")
            self.reg_confirm_entry.configure(show="*")
    
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
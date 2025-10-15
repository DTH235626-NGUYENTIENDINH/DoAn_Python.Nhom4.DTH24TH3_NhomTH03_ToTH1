from tkinter import *
# Dùng relative import để gọi các module khác
from ..Handle import handle_login_register as hr
from . import register_ui 
#Hàm cửa sổ đăng nhập
def Open_Login():
    login = Tk()
    login.title("Quản lý sách")
    login.resizable(width=False, height=False)
    login.minsize(width=400, height=370)

    lblLogin = Label(login, text="Đăng nhập", font=("Arial", 20), fg="#09611C")
    lblLogin.place(x=150, y=50)

    lblUsername = Label(login, text="Tên đăng nhập:", font=("Arial", 12))
    lblUsername.place(x=50, y=120)

    txtUsername = Entry(login, width=30)
    txtUsername.place(x=180, y=123)

    lblPassword = Label(login, text="Mật khẩu:", font=("Arial", 12))
    lblPassword.place(x=50, y=170)

    txtPassword = Entry(login, width=30, show="*")
    txtPassword.place(x=180, y=173)

    checked_state = IntVar()
    chbtnPassword = Checkbutton(login, text="Hiện mật khẩu",
                                variable=checked_state,
                                command=lambda: hr.toggle_password_visibility(checked_state, txtPassword))
    chbtnPassword.place(x=180, y=200)

    btnLogin = Button(login, text="Đăng nhập", width=15, bg="#09611C", fg="white",
                      command=lambda: hr.handle_login(txtUsername, txtPassword))
    btnLogin.place(x=150, y=240)

    lblRegister = Label(login, text="Chưa có tài khoản? Đăng ký ngay", fg="blue", cursor="hand2")
    lblRegister.place(x=120, y=290)
    lblRegister.bind("<Button-1>", lambda event: Close_Login(login))

    login.mainloop()
#Hàm đóng cửa sổ đăng nhập
def Close_Login(current_window):
    current_window.destroy()
    register_ui.Open_Register()



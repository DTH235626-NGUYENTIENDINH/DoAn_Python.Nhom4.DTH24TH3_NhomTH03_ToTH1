from tkinter import *
# Dùng relative import để gọi các module khác
from ..Handle import handle_login_register as hr
from . import login_ui
#Hàm cửa sổ đăng ký
def Open_Register():
    register = Tk()
    register.title("Quản lý sách")
    register.resizable(width=False, height=False)
    register.minsize(width=400, height=450)

    lblRegister = Label(register, text="Đăng ký", font=("Arial", 20), fg="#09611C")
    lblRegister.place(x=150, y=50)

    lblUsername = Label(register, text="Tên đăng nhập:", font=("Arial", 12))
    lblUsername.place(x=50, y=120)

    txtUsername = Entry(register, width=30)
    txtUsername.place(x=180, y=123)

    lblHoTen = Label(register, text="Họ và tên:", font=("Arial", 12))
    lblHoTen.place(x=50, y=170)

    txtHoTen = Entry(register, width=30)
    txtHoTen.place(x=180, y=173)

    lblSDT = Label(register, text="Số điện thoại:", font=("Arial", 12))
    lblSDT.place(x=50, y=220)

    txtSDT = Entry(register, width=30)
    txtSDT.place(x=180, y=223)

    lblPassword = Label(register, text="Mật khẩu:", font=("Arial", 12))
    lblPassword.place(x=50, y=270)

    txtPassword = Entry(register, width=30, show="*")
    txtPassword.place(x=180, y=273)

    checked_state = IntVar()
    chbtnPassword = Checkbutton(register, text="Hiện mật khẩu",
                            variable=checked_state,
                            command=lambda: hr.toggle_password_visibility(checked_state, txtPassword))
    chbtnPassword.place(x=180, y=300)

    btnRegister = Button(register, text="Đăng ký", width=15, bg="#09611C", fg="white",
                    command=lambda: hr.handle_register(txtHoTen, txtUsername, txtSDT, txtPassword))                 
    btnRegister.place(x=150, y=340)

    lblLogin = Label(register, text="Đã có tài khoản? Đăng nhập ngay", fg="blue", cursor="hand2")
    lblLogin.place(x=120, y=390)
    lblLogin.bind("<Button-1>", lambda event: Close_Register(register))

    register.mainloop()

#Hàm dóng cửa sổ đăng ký
def Close_Register(current_window):
    current_window.destroy()
    login_ui.Open_Login()

import customtkinter as ctk
from gui.ui_login_register import App as LoginApp
from gui.main import OpenMainWindow

while True:
    login_success = False

    def on_login_success(message):
        global login_success
        login_success = True

    login_app = LoginApp(on_login_success)
    login_app.mainloop()

    if login_success:
        OpenMainWindow()
    else:
        break   

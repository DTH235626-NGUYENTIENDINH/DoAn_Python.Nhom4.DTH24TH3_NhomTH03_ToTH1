from tkinter import *
# Dùng relative import để gọi các module khác

def reader_ui():
    readers_main = Tk()
    readers_main.title("Giao diện đọc giả")
    readers_main.resizable(width=False, height=False)
    readers_main.minsize(width=600, height=400)

    lblWelcome = Label(readers_main, text="Chào mừng đến với giao diện đọc giả!", font=("Arial", 16), fg="#09611C")
    lblWelcome.pack(pady=20)

    # Thêm các thành phần giao diện khác cho đọc giả tại đây

    readers_main.mainloop()
#
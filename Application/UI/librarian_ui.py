import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Quản lý sách")
root.geometry("800x600")

tabControl = ttk.Notebook(root)
#Hai farme tương ứng với hai tab
tab_BookManagement = ttk.Frame(tabControl)
tab_ReaderManagement = ttk.Frame(tabControl)
tab_BorrowManagement = ttk.Frame(tabControl)
#Thêm hai frame vào tab control
tabControl.add(tab_BookManagement, text='Quản Lý Sách')
tabControl.add(tab_ReaderManagement, text='Quản Lý Độc Giả')
tabControl.add(tab_BorrowManagement, text='Quản Lý Phiếu Mượn')
#Ném tab control vào cửa sổ chính
tabControl.pack(expand=1, fill="both", padx=10, pady=10)
#================================================================
#---GIAO DIỆN 1: QUẢN LÝ SÁCH (Nội dung cho tab_BookManagement)---
#================================================================
#Khung nhập thông tin sách
lbl_TextBOOK = ttk.Label(tab_BookManagement, text="QUẢN LÝ SÁCH", font=("Arial", 20, 'bold'), foreground="#09611C")
lbl_TextBOOK.pack(pady=10)
info_frame_book = ttk.LabelFrame(tab_BookManagement, text="Thông tin sách")
info_frame_book.pack(padx=15, pady=10, fill="x")
book_labels = ["Tên sách:", "Tác giả:", "Thể loại:", "Số lượng:"]
for i, label_text in enumerate(book_labels):
    label = ttk.Label(info_frame_book, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
    entry = ttk.Entry(info_frame_book, width=50)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
info_frame_book.grid_columnconfigure(1, weight=1)
#Khung chức năng sách
button_frame_book = ttk.Frame(tab_BookManagement)
button_frame_book.pack(padx=15, pady=10, fill="x")
# Nút Thêm (màu xanh lá)
tk.Button(
    button_frame_book, 
    text="Thêm Sách", 
    bg="green",            # bg = background color
    fg="white",            # fg = foreground (text) color
    activebackground="darkgreen",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')

# Nút Sửa (màu xanh dương)
tk.Button(
    button_frame_book, 
    text="Sửa Sách", 
    bg="#007bff", 
    fg="white",
    activebackground="#0056b3",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')

# Nút Xoá (màu đỏ)
tk.Button(
    button_frame_book, 
    text="Xoá Sách", 
    bg="#dc3545", 
    fg="white",
    activebackground="#a71d2a",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')

# Nút Tra cứu (màu xám)
tk.Button(
    button_frame_book, 
    text="Tra cứu", 
    bg="#6c757d", 
    fg="white",
    activebackground="#545b62",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')
tree_frame_book = ttk.Frame(tab_BookManagement)
tree_frame_book.pack(padx=15, pady=10, fill="both", expand=True)
columns_book = ("Mã sách", "Tên sách", "Tác giả", "Thể loại", "Số lượng")
tree_book = ttk.Treeview(tree_frame_book, columns=columns_book, show='headings')
for col in columns_book:
    tree_book.heading(col, text=col)
    tree_book.column(col, width=100, anchor="center")
tree_book.pack(side="left", fill="both", expand=True)
scrollbar_book = ttk.Scrollbar(tree_frame_book, orient="vertical", command=tree_book.yview)
tree_book.configure(yscroll=scrollbar_book.set)
scrollbar_book.pack(side="right", fill="y")
#===================================================================
#---GIAO DIỆN 2: QUẢN LÝ ĐỘC GIẢ (Nội dung cho tab_ReaderManagement)---
#===================================================================
#Khung nhập thông tin độc giả
lbl_TextREADER = ttk.Label(tab_ReaderManagement, text="QUẢN LÝ ĐỘC GIẢ", font=("Arial", 20, 'bold'), foreground="#09611C")
lbl_TextREADER.pack(pady=10)
info_frame_reader = ttk.LabelFrame(tab_ReaderManagement, text="Thông tin độc giả")
info_frame_reader.pack(padx=15, pady=10, fill="x")
reader_labels = ["Họ và Tên:", "Username:", "Số điện thoại:"]
for i, label_text in enumerate(reader_labels):
    label = ttk.Label(info_frame_reader, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
    entry = ttk.Entry(info_frame_reader, width=50)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
info_frame_reader.grid_columnconfigure(1, weight=1)
#Khung chức năng độc giả
button_frame_reader = ttk.Frame(tab_ReaderManagement)
button_frame_reader.pack(padx=15, pady=10, fill="x")
# Nút sưaea (màu xanh dương)
tk.Button(
    button_frame_reader, 
    text="Sửa Thông Tin",
    bg="#007bff",
    fg="white",
    activebackground="#0056b3", 
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')
# Nút Xoá (màu đỏ)
tk.Button(
    button_frame_reader, 
    text="Xoá Độc Giả", 
    bg="#dc3545", 
    fg="white",
    activebackground="#a71d2a",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')
# Nút Tra cứu (màu xám)
tk.Button(
    button_frame_reader, 
    text="Tra cứu", 
    bg="#6c757d", 
    fg="white",
    activebackground="#545b62",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')
# Nút chia sẻ quyền (màu cam)
tk.Button(
    button_frame_reader, 
    text="Chia sẻ quyền", 
    bg="#fd7e14", 
    fg="white",
    activebackground="#b53e07",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')
tree_frame_reader = ttk.Frame(tab_ReaderManagement)
tree_frame_reader.pack(padx=15, pady=10, fill="both", expand=True)
columns_reader = ("Mã độc giả", "Họ và Tên", "Username", "Số điện thoại")
tree_reader = ttk.Treeview(tree_frame_reader, columns=columns_reader, show='headings')
for col in columns_reader:
    tree_reader.heading(col, text=col)
    tree_reader.column(col, width=100, anchor="center")     
tree_reader.pack(side="left", fill="both", expand=True)
scrollbar_reader = ttk.Scrollbar(tree_frame_reader, orient="vertical", command=tree_reader.yview)
tree_reader.configure(yscroll=scrollbar_reader.set)
scrollbar_reader.pack(side="right", fill="y")
#===================================================================
#---GIAO DIỆN 3: QUẢN LÝ PHIẾU MƯỢN (Nội dung cho tab_BorrowManagement)---
#===================================================================
#Khung nhập thông tin phiếu mượn
lbl_TextBORROW = ttk.Label(tab_BorrowManagement, text="QUẢN LÝ PHIẾU MƯỢN", font=("Arial", 20, 'bold'), foreground="#09611C")
lbl_TextBORROW.pack(pady=10)
info_frame_borrow = ttk.LabelFrame(tab_BorrowManagement, text="Thông tin phiếu mượn")
info_frame_borrow.pack(padx=15, pady=10, fill="x")  
borrow_labels = ["Mã độc giả:", "Mã sách:", "Ngày mượn:", "Ngày hẹn trả:", "Trạng thái:"]
for i, label_text in enumerate(borrow_labels):
    label = ttk.Label(info_frame_borrow, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
    entry = ttk.Entry(info_frame_borrow, width=50)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
info_frame_borrow.grid_columnconfigure(1, weight=1)
#Khung chức năng phiếu mượn
button_frame_borrow = ttk.Frame(tab_BorrowManagement)
button_frame_borrow.pack(padx=15, pady=10, fill="x")
# Nút Thêm (màu xanh lá)
tk.Button(
    button_frame_borrow, 
    text="Thêm Phiếu Mượn", 
    bg="green",            # bg = background color
    fg="white",            # fg = foreground (text) color
    activebackground="darkgreen",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')
# Nút Tra cứu (màu xám)
tk.Button(
    button_frame_borrow, 
    text="Tra cứu", 
    bg="#6c757d", 
    fg="white",
    activebackground="#545b62",
    activeforeground="white",
    font=('Helvetica', 10, 'bold')
).pack(side="left", padx=5, expand=True, fill='x')
tree_frame_borrow = ttk.Frame(tab_BorrowManagement)
tree_frame_borrow.pack(padx=15, pady=10, fill="both", expand=True)
columns_borrow = ("Mã phiếu mượn", "Mã độc giả", "Mã sách", "Ngày mượn", "Ngày hẹn trả", "Trạng thái")
tree_borrow = ttk.Treeview(tree_frame_borrow, columns=columns_borrow, show='headings')
for col in columns_borrow:
    tree_borrow.heading(col, text=col)
    tree_borrow.column(col, width=100, anchor="center") 
tree_borrow.pack(side="left", fill="both", expand=True)
scrollbar_borrow = ttk.Scrollbar(tree_frame_borrow, orient="vertical", command= tree_borrow.yview)
tree_borrow.configure(yscroll=scrollbar_borrow.set)     
scrollbar_borrow.pack(side="right", fill="y")
#==================================================================
#---Chạy ứng dụng ---
root.mainloop()


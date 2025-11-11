#==========================Thư viện==========================
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from tkcalendar import DateEntry
from handlers.persistence_manager import *
#==========================Cấu hình Màu sắc và Biến Toàn cục==========================
# --- Cấu hình Màu sắc (Đã chỉnh sửa để dễ quản lý) ---
SIDEBAR_BG = "#3C8EFA"
NORMAL_BUTTON_FG = "#3C8EFA"
ACTIVE_COLOR = "#5AA0FF" 
HOVER_COLOR = "#5AA0FF" # Giữ nguyên hover_color cho nút bình thường
LOGOUT_COLOR = "#FA3C3C"

# --- Khai báo Biến Toàn cục ---
current_active_button = None
content_frames = {}
root = None # Khai báo root ở phạm vi toàn cục hoặc xử lý bên trong hàm
book_widget = {}

#==========================Hàm quản lý chuyển đổi giao diện======================
def switch_view(view_name, new_button):
    global current_active_button
    
    # 1. Quản lý trạng thái Active của nút (Đổi màu)
    if current_active_button:
        # Khôi phục nút active trước đó về màu nền
        current_active_button.configure(fg_color=NORMAL_BUTTON_FG)
        
    # 2. Thiết lập màu Active cho nút mới được click
    new_button.configure(fg_color=ACTIVE_COLOR)
    current_active_button = new_button
    
    # 3. Ẩn tất cả các Frame nội dung
    for frame in content_frames.values():
        frame.grid_forget()

    # 4. Hiển thị Frame của giao diện được chọn
    if view_name in content_frames:
        # Đặt Frame vào vị trí của main_content_area
        content_frames[view_name].grid(row=0, column=0, sticky="nsew")
        print(f"Hiển thị giao diện: {view_name}")
    else:
        print(f"Lỗi: Không tìm thấy Frame cho giao diện '{view_name}'")

#==========================Hàm giao diện======================
def OpenMainWindow():
    global root, current_active_button, content_frames, book_widget
    
    #Tạo cửa sổ chính
    root = ctk.CTk()
    root.title("📖 Phần mềm quản lý sách")
    root.geometry("1280x720")
    root.resizable(True, True)
    root.configure(fg_color="#E1F4FD")
    
    # --- Cấu hình Grid Tổng thể cho root ---
    root.grid_columnconfigure(0, weight=0) # Cột 0: Sidebar (cố định)
    root.grid_columnconfigure(1, weight=1) # Cột 1: Nội dung chính (giãn nở)
    root.grid_rowconfigure(0, weight=1)    # Hàng 0: Giãn nở
    
    # === Sidebar Frame (Dùng CTkScrollableFrame) ===
    left_frame = ctk.CTkScrollableFrame(
        root, 
        width=250, 
        fg_color=SIDEBAR_BG,
        scrollbar_button_color=SIDEBAR_BG, 
        scrollbar_button_hover_color=HOVER_COLOR
    )
    left_frame.grid(row=0, column=0, sticky="nsew")
    
    # Cấu hình grid cho Sidebar
    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_rowconfigure(7, weight=1) 
    
    #===========================Sidebar control==========================
    # (Phần Logo và Tiêu đề giữ nguyên, đã chuyển sang dùng grid)
    # ... code logo và tên ứng dụng ...
    try:
        logo_picture = ctk.CTkImage(Image.open("Picture/BookLogo.png"), size=(40, 40))
        logo_label = ctk.CTkLabel(left_frame, image=logo_picture, text="")
        logo_label.grid(row=0, column=0, pady=(20, 10))
    except FileNotFoundError:
        logo_label = ctk.CTkLabel(left_frame, text="[Logo]", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        logo_label.grid(row=0, column=0, pady=(20, 10))

    app_logo = ctk.CTkLabel(left_frame, text="Quản lý sách", font=ctk.CTkFont(size=20, weight="bold"), fg_color=SIDEBAR_BG, text_color="white")
    app_logo.grid(row=1, column=0, pady=(0, 40))

    # Nút giao diện welcome (Row 2)
    btn_mainMenu = ctk.CTkButton(left_frame, text="🏠 Trang chủ", fg_color=NORMAL_BUTTON_FG, hover_color=HOVER_COLOR, font=ctk.CTkFont(size=16, weight="bold"))
    btn_mainMenu.grid(row=2, column=0, pady=(50, 20), padx=20, sticky="ew")

    # Nút quản lý sách (Row 3)
    btn_bookManagement = ctk.CTkButton(left_frame, text="📘 Quản lý sách", fg_color=NORMAL_BUTTON_FG, hover_color=HOVER_COLOR, font=ctk.CTkFont(size=16, weight="bold"))
    btn_bookManagement.grid(row=3, column=0, pady=(0, 20), padx=20, sticky="ew")
    
    # ... Các nút khác (giữ nguyên cấu trúc) ...
    btn_readerManagement = ctk.CTkButton(left_frame, text="👤 Quản lý độc giả", fg_color=NORMAL_BUTTON_FG, hover_color=HOVER_COLOR, font=ctk.CTkFont(size=16, weight="bold"))
    btn_readerManagement.grid(row=4, column=0, pady=(0, 20), padx=20, sticky="ew")
    btn_borrowReturnManagement = ctk.CTkButton(left_frame, text="📚 Mượn trả sách", fg_color=NORMAL_BUTTON_FG, hover_color=HOVER_COLOR, font=ctk.CTkFont(size=16, weight="bold"))
    btn_borrowReturnManagement.grid(row=5, column=0, pady=(0, 20), padx=20, sticky="ew")
    btn_statisticsReports = ctk.CTkButton(left_frame, text="📊 Thống kê báo cáo", fg_color=NORMAL_BUTTON_FG, hover_color=HOVER_COLOR, font=ctk.CTkFont(size=16, weight="bold"))
    btn_statisticsReports.grid(row=6, column=0, pady=(0, 20), padx=20, sticky="ew")
    
    # Nút cài đặt (Row 8)
    btn_settings = ctk.CTkButton(left_frame, text="⚙️ Cài đặt", fg_color=NORMAL_BUTTON_FG, hover_color=HOVER_COLOR, font=ctk.CTkFont(size=16, weight="bold"))
    btn_settings.grid(row=8, column=0, pady=(100, 10), padx=20, sticky="ew")
    
    # Nút Đăng xuất (Row 9)
    btn_logout = ctk.CTkButton(left_frame, text="⬅ Đăng xuất", fg_color=LOGOUT_COLOR, hover_color="#CC3030", font=ctk.CTkFont(size=16, weight="bold"))
    btn_logout.grid(row=9, column=0, pady=(10, 20), padx=20, sticky="ew")


#===========================Khu vực quản lý Frame Nội dung (Column 1)==========================
    # Container chính cho Nội dung
    main_content_area = ctk.CTkFrame(root, fg_color="transparent")
    main_content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content_area.grid_columnconfigure(0, weight=1)
    main_content_area.grid_rowconfigure(0, weight=1)
#============================================================================================================================================ 
    # --- 1. Tạo Frame Trang chủ (Welcome) ---
#============================================================================================================================================    
    hone_frame = ctk.CTkFrame(main_content_area)
    welcome_label = ctk.CTkLabel(hone_frame, text="CHÀO MỪNG ĐẾN VỚI PHẦN MỀM QUẢN LÝ SÁCH", font=ctk.CTkFont(size=30))
    welcome_label.pack(expand=True)
    content_frames["Trang chủ"] = hone_frame # Lưu Frame
#============================================================================================================================================ 
    # --- 2. Tạo Frame Quản lý Sách ---
#============================================================================================================================================    
    ROOT_BG_COLOR = "#E1F4FD" # Lấy màu nền root bạn đã thiết lập

    book_management_frame = ctk.CTkFrame(main_content_area, fg_color=ROOT_BG_COLOR) 

    # Cấu hình grid cho book_management_frame (2 cột, 3 hàng)
    book_management_frame.grid_columnconfigure(0, weight=3) # Cột 0: Nhập liệu/List (Rộng hơn)
    book_management_frame.grid_columnconfigure(1, weight=1) # Cột 1: Nút (Hẹp hơn)
    book_management_frame.grid_rowconfigure(0, weight=0) # Hàng 0: Tiêu đề (Không giãn nở)
    book_management_frame.grid_rowconfigure(1, weight=0) # Hàng 1: Form & Nút (Không giãn nở)
    book_management_frame.grid_rowconfigure(2, weight=1) # Hàng 2: List (GIÃN NỞ)

    #========================================================
    # === HÀNG 0: Tiêu đề Chung ===
    #========================================================
    frame_title = ctk.CTkLabel(book_management_frame, 
                            text="QUẢN LÝ THÔNG TIN SÁCH", 
                            font=ctk.CTkFont(size=24, weight="bold"), 
                            text_color="#3C8EFA")
    # Đặt tiêu đề chiếm 2 cột
    frame_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")


    #========================================================
    # === HÀNG 1, CỘT 0: Form Nhập Liệu ===
    #========================================================
    input_form_frame = ctk.CTkFrame(book_management_frame, fg_color="#FFFFFF", corner_radius=10)
    input_form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Cấu hình grid cho Form bên trong (4 cột)
    input_form_frame.grid_columnconfigure(0, weight=0) # Cột Label 1 (Không giãn nở)
    input_form_frame.grid_columnconfigure(1, weight=1) # Cột Entry 1 (Giãn nở)
    input_form_frame.grid_columnconfigure(2, weight=0) # Cột Label 2 (Không giãn nở)
    input_form_frame.grid_columnconfigure(3, weight=1) # Cột Entry 2 (Giãn nở)

    # Row 0: Mã sách và Tên sách
    # Mã sách (Cột 0 & 1)
    ma_sach_label = ctk.CTkLabel(input_form_frame, text="Mã sách (7 Ký tự)*:", font=ctk.CTkFont(size=13))
    ma_sach_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ma_sach = ctk.CTkEntry(input_form_frame, placeholder_text="VD: AB12001")
    entry_ma_sach.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="ew")

    # Tên sách (Cột 2 & 3)
    ten_sach_label = ctk.CTkLabel(input_form_frame, text="Tên sách*:", font=ctk.CTkFont(size=13))
    ten_sach_label.grid(row=0, column=2, padx=(20, 10), pady=10, sticky="w")
    entry_ten_sach = ctk.CTkEntry(input_form_frame, placeholder_text="Tên cuốn sách")
    entry_ten_sach.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="ew")

    # Row 1: Tác giả và Nhà xuất bản
    # Tác giả (Cột 0 & 1)
    tac_gia_label = ctk.CTkLabel(input_form_frame, text="Tác giả*:", font=ctk.CTkFont(size=13))
    tac_gia_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_tac_gia = ctk.CTkEntry(input_form_frame, placeholder_text="Tên tác giả")
    entry_tac_gia.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")

    # Nhà xuất bản (Cột 2 & 3)
    nxb_label = ctk.CTkLabel(input_form_frame, text="Nhà xuất bản*:", font=ctk.CTkFont(size=13))
    nxb_label.grid(row=1, column=2, padx=(20, 10), pady=10, sticky="w")
    entry_nxb = ctk.CTkEntry(input_form_frame, placeholder_text="Tên nhà xuất bản")
    entry_nxb.grid(row=1, column=3, padx=(0, 20), pady=10, sticky="ew")


    # Row 2: Năm xuất bản và Số lượng tồn
    # Năm xuất bản (Cột 0 & 1)
    nam_xb_label = ctk.CTkLabel(input_form_frame, text="Năm xuất bản*:", font=ctk.CTkFont(size=13))
    nam_xb_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_nam_xb = ctk.CTkEntry(input_form_frame, placeholder_text="Năm xuất bản (VD: 2023)")
    entry_nam_xb.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")

    # Số lượng tồn (Cột 2 & 3)
    so_luong_label = ctk.CTkLabel(input_form_frame, text="Số lượng tồn:", font=ctk.CTkFont(size=13))
    so_luong_label.grid(row=2, column=2, padx=(20, 10), pady=10, sticky="w")
    entry_so_luong = ctk.CTkEntry(input_form_frame, placeholder_text="Số lượng trong kho (Mặc định 0)")
    entry_so_luong.grid(row=2, column=3, padx=(0, 20), pady=10, sticky="ew")


    # Row 3: Thể loại (Chiếm toàn bộ chiều ngang)
    the_loai_label = ctk.CTkLabel(input_form_frame, text="Thể loại*:", font=ctk.CTkFont(size=13))
    the_loai_label.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_the_loai = ctk.CTkEntry(input_form_frame, placeholder_text="Loại sách (VD: Khoa học, Tiểu thuyết)")
    entry_the_loai.grid(row=3, column=1, columnspan=3, padx=(0, 20), pady=10, sticky="ew")

    book_widget = {
        'MaSach': entry_ma_sach,
        'TenSach': entry_ten_sach,
        'TacGia': entry_tac_gia,
        'TheLoai': entry_the_loai,
        'NhaXuatBan': entry_nxb,
        'NamXuatBan': entry_nam_xb,
        'SoLuong': entry_so_luong
    }

    #========================================================
    # === HÀNG 1, CỘT 1: Khu vực Nút Thao tác ===
    #========================================================
    button_area_frame = ctk.CTkFrame(book_management_frame, fg_color="#F0F0F0", corner_radius=10)
    button_area_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=10)

    # Cấu hình grid cho khu vực nút (để các nút xếp chồng lên nhau và giãn nở)
    button_area_frame.grid_columnconfigure(0, weight=1)

    # Nút Thêm
    btn_add = ctk.CTkButton(button_area_frame, 
                            text="➕ Thêm Mới", 
                            fg_color="#4CAF50", 
                            hover_color="#388E3C",
                            command=lambda: add_book(book_widget))
    btn_add.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

    # Nút Sửa 
    btn_update = ctk.CTkButton(button_area_frame, 
                               text="🔄 Cập nhật", 
                               fg_color="#FFC107", 
                               hover_color="#FFB300",
                               command=lambda: update_book(book_widget))
    btn_update.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

    # Nút Xóa
    btn_delete = ctk.CTkButton(button_area_frame, 
                               text="🗑️ Xóa Sách", 
                               fg_color="#F44336", 
                               hover_color="#D32F2F")
    btn_delete.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

    # Nút Tra cứu 
    btn_search = ctk.CTkButton(button_area_frame, 
                            text="🔍 Tra cứu", 
                            fg_color="#3C8EFA", 
                            hover_color="#5AA0FF")
    btn_search.grid(row=3, column=0, pady=(10, 20), padx=20, sticky="ew")


    #========================================================
    # === HÀNG 2, CỘT 0 & 1: Khu vực List/Bảng (Giãn nở) ===
    #========================================================

    list_area_frame = ctk.CTkFrame(book_management_frame, fg_color="#FFFFFF", corner_radius=10)
    # Đặt Frame list chiếm cả 2 cột
    list_area_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
    list_title = ctk.CTkLabel(list_area_frame, text="DANH SÁCH CÁC SÁCH", 
                            font=ctk.CTkFont(size=14, weight="bold"), text_color="#3C8EFA")
    list_title.pack(padx=20, pady=20)
    column = ("Mã sách", "Tên sách", "Tác giả", "Thể loại", "Nhà xuất bản", "Năm xuất bản", "Số lượng tồn")
    tree_view = ttk.Treeview(list_area_frame, columns=column, show="headings", height=10)
    for col in column:
        tree_view.heading(col, text=col)
        tree_view.column(col, width=100, anchor="center")             
    tree_view.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    scrollbar = ctk.CTkScrollbar(list_area_frame, orientation="vertical", command=tree_view.yview)
    tree_view.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y", pady=(0, 20))

    register_book_treeview(tree_view)
    register_book_entries(book_widget)
    load_book_data()  # Tải dữ liệu sách vào Treeview khi khởi tạo giao diện
    tree_view.bind("<<TreeviewSelect>>", on_book_select)
    content_frames["Quản lý sách"] = book_management_frame # Lưu Frame
#============================================================================================================================================ 
    # --- 3. Tạo Frame Quản lý Độc giả ---
#============================================================================================================================================    
    reader_management_frame = ctk.CTkFrame(main_content_area, fg_color=ROOT_BG_COLOR)

    #Cấu hinh grid cho reader_management_frame (2 cột, 3 hàng)
    reader_management_frame.grid_columnconfigure(0, weight=3) # Cột 0
    reader_management_frame.grid_columnconfigure(1, weight=1) # Cột 1
    reader_management_frame.grid_rowconfigure(0, weight=0) # Hàng 0
    reader_management_frame.grid_rowconfigure(1, weight=0) # Hàng 1
    reader_management_frame.grid_rowconfigure(2, weight=1) # Hàng 2
    # Tiêu đề
    reader_frame_title = ctk.CTkLabel(reader_management_frame, 
                            text="QUẢN LÝ THÔNG TIN ĐỘC GIẢ", 
                            font=ctk.CTkFont(size=24, weight="bold"), 
                            text_color="#3C8EFA")
    reader_frame_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    content_frames["Quản lý độc giả"] = reader_management_frame # Lưu Frame
    # form nhập liệu
    intput_reader_form_frame = ctk.CTkFrame(reader_management_frame, fg_color="#FFFFFF", corner_radius=10)
    intput_reader_form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    # cấu hình grid cho form bên trong (4 cột)
    intput_reader_form_frame .grid_columnconfigure(0, weight=0) # Cột Label 1 (Không giãn nở)
    intput_reader_form_frame .grid_columnconfigure(1, weight=1) # Cột Entry 1 (Giãn nở)
    intput_reader_form_frame .grid_columnconfigure(2, weight=0) # Cột Label 2 (Không giãn nở)
    intput_reader_form_frame .grid_columnconfigure(3, weight=1) # Cột Entry 2 (Giãn nở)
    # Mã độc giả 
    ma_doc_gia_label = ctk.CTkLabel(intput_reader_form_frame , text="Mã độc giả (7 Ký tự):", font=ctk.CTkFont(size=13))
    ma_doc_gia_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ma_doc_gia = ctk.CTkEntry(intput_reader_form_frame , placeholder_text="VD: DG12001")
    entry_ma_doc_gia.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="ew")
    # Họ tên 
    ho_ten_label = ctk.CTkLabel(intput_reader_form_frame , text="Họ tên:", font=ctk.CTkFont(size=13))
    ho_ten_label.grid(row=0, column=2, padx=(20, 10), pady=10, sticky="w")
    entry_ho_ten = ctk.CTkEntry(intput_reader_form_frame , placeholder_text="Họ và tên độc giả (Bắt buộc)")
    entry_ho_ten.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="ew")
    # Địa chỉ
    dia_chi_label = ctk.CTkLabel(intput_reader_form_frame , text="Địa chỉ:", font=ctk.CTkFont(size=13))
    dia_chi_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_dia_chi = ctk.CTkEntry(intput_reader_form_frame , placeholder_text="Địa chỉ liên hệ")
    entry_dia_chi.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
    # Số điện thoại
    so_dien_thoai_label = ctk.CTkLabel(intput_reader_form_frame , text="Số điện thoại:", font=ctk.CTkFont(size=13))
    so_dien_thoai_label.grid(row=1, column=2, padx=(20, 10), pady=10, sticky="w")
    entry_so_dien_thoai = ctk.CTkEntry(intput_reader_form_frame , placeholder_text="Số điện thoại liên hệ")
    entry_so_dien_thoai.grid(row=1, column=3, padx=(0, 20), pady=10, sticky="ew")
    #Ngay sỉnh 
    ngay_sinh_label = ctk.CTkLabel(intput_reader_form_frame , text="Ngày sinh:", font=ctk.CTkFont(size=13))
    ngay_sinh_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ngay_sinh = DateEntry(intput_reader_form_frame , selexmode='day', date_pattern='dd-mm-yyyy',
                                width=18, background='white', foreground='black', borderwidth=1)
    entry_ngay_sinh.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")

    # Nút Thao tác
    reader_button_area_frame = ctk.CTkFrame(reader_management_frame, fg_color="#F0F0F0", corner_radius=10)
    reader_button_area_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=10)
    # Cấu hình grid cho khu vực nút (để các nút xếp chồng lên nhau và giãn nở)
    reader_button_area_frame.grid_columnconfigure(0, weight=1)
    # Nút Thêm
    btn_add_reader = ctk.CTkButton(reader_button_area_frame, 
                                   text=" ➕ Thêm Mới", 
                                   fg_color="#4CAF50", 
                                   hover_color="#388E3C")
    btn_add_reader.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")
    # Nút Sửa   
    btn_update_reader = ctk.CTkButton(reader_button_area_frame, 
                                      text="🔄 Cập nhật", 
                                      fg_color="#FFC107", 
                                      hover_color="#FFB300")
    btn_update_reader.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
    # Nút Xóa
    btn_delete_reader = ctk.CTkButton(reader_button_area_frame, 
                                      text="🗑️ Xóa Độc Giả", 
                                      fg_color="#F44336", 
                                      hover_color="#D32F2F")   
    btn_delete_reader.grid(row=2, column=0, pady=10, padx=20, sticky="ew")
    # Nút Tra cứu
    btn_search_reader = ctk.CTkButton(reader_button_area_frame, 
                            text="🔍 Tra cứu", 
                            fg_color="#3C8EFA", 
                            hover_color="#5AA0FF")
    btn_search_reader.grid(row=3, column=0, pady=(10, 20), padx=20, sticky="ew")
    
    # Khu vực List/Bảng (Giãn nở)
    reader_list_area_frame = ctk.CTkFrame(reader_management_frame, fg_color="#FFFFFF", corner_radius=10)
    # Đặt Frame list chiếm cả 2 cột
    reader_list_area_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
    # Ví dụ nội dung trong List
    reader_list_title = ctk.CTkLabel(reader_list_area_frame, text="DANH SÁCH CÁC ĐỘC GIẢ", 
                            font=ctk.CTkFont(size=14, weight="bold"), text_color="#3C8EFA") 
    reader_list_title.pack(padx=20, pady=20)
#============================================================================================================================================ 
    # -- 4. Tạo Frame Mượn Trả Sách ---
#============================================================================================================================================ 
    ROOT_BG_COLOR = "#E1F4FD" 

    borrow_return_frame = ctk.CTkFrame(main_content_area, fg_color=ROOT_BG_COLOR) 

    # Cấu hình grid cho borrow_return_frame (3 cột, 3 hàng)
    borrow_return_frame.grid_columnconfigure(0, weight=1) # Cột 0: Thông tin Độc giả
    borrow_return_frame.grid_columnconfigure(1, weight=0) # Cột 1: Nút (Cố định, hẹp)
    borrow_return_frame.grid_columnconfigure(2, weight=1) # Cột 2: Thông tin Sách
    borrow_return_frame.grid_rowconfigure(0, weight=0) 
    borrow_return_frame.grid_rowconfigure(1, weight=0) 
    borrow_return_frame.grid_rowconfigure(2, weight=1) # Hàng 2: List (GIÃN NỞ)

    #========================================================
    # === HÀNG 0: Tiêu đề Chung ===
    #========================================================
    frame_title_br = ctk.CTkLabel(borrow_return_frame, 
                                text="QUẢN LÝ MƯỢN TRẢ SÁCH", 
                                font=ctk.CTkFont(size=24, weight="bold"), 
                                text_color="#3C8EFA")
    frame_title_br.grid(row=0, column=0, columnspan=3, padx=20, pady=(15, 10), sticky="w")


    #========================================================
    # ===   HÀNG 1, CỘT 0: Form Độc giả & Phiếu Mượn      ===
    #========================================================
    borrow_form = ctk.CTkFrame(borrow_return_frame, fg_color="#FFFFFF", corner_radius=10)   
    borrow_form.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    borrow_form.grid_columnconfigure(0, weight=0) # Cột Label 1 (Không giãn nở)
    borrow_form.grid_columnconfigure(1, weight=1) # Cột Entry 1 (Giãn nở)

    ctk.CTkLabel(borrow_form, text="THÔNG TIN PHIẾU MƯỢN", 
                font=ctk.CTkFont(size=16, weight="bold"), 
                text_color="#3C8EFA").grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
    # Mã phiếu mượn
    ma_phieu_label = ctk.CTkLabel(borrow_form, text="Mã phiếu mượn:", font=ctk.CTkFont(size=13))
    ma_phieu_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ma_phieu = ctk.CTkEntry(borrow_form, placeholder_text="VD: PM12001")
    entry_ma_phieu.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
    # Mã độc giả
    ma_doc_gia_label_br = ctk.CTkLabel(borrow_form, text="Mã độc giả:", font=ctk.CTkFont(size=13))
    ma_doc_gia_label_br.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
    doc_gia_options = ["Chọn mã độc giả", "DG12001", "DG12002", "DG12003"]
    entry_ma_doc_gia_br = ctk.CTkComboBox(borrow_form, values=doc_gia_options)
    entry_ma_doc_gia_br.set(doc_gia_options[0]) # Đặt giá trị mặc định là "Chọn mã độc giả"

    entry_ma_doc_gia_br.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
    # Ngày mượn
    ngay_muon_label = ctk.CTkLabel(borrow_form, text="Ngày mượn:", font=ctk.CTkFont(size=13))
    ngay_muon_label.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ngay_muon = DateEntry(borrow_form, selexmode='day', date_pattern='dd-mm-yyyy',
                                width=18, background='white', foreground='black', borderwidth=1)
    entry_ngay_muon.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
    # Ngày hẹn trả
    ngay_tra_du_kien_label = ctk.CTkLabel(borrow_form, text="Ngày trả dự kiến:", font=ctk.CTkFont(size=13))
    ngay_tra_du_kien_label.grid(row=4, column=0, padx=(20, 10), pady=10, sticky="w")
    ngay_tra_du_kien_label = DateEntry(borrow_form, selexmode='day', date_pattern='dd-mm-yyyy',
                                width=18, background='white', foreground='black', borderwidth=1)
    ngay_tra_du_kien_label.grid(row=4, column=1, padx=(0, 20), pady=10, sticky="ew")


    #=========================================================
    # === HÀNG 1, CỘT 1: Khu vực Nút Thao tác (Mượn/Trả)   ===
    #=========================================================
    button_area_br = ctk.CTkFrame(borrow_return_frame, fg_color="#F0F0F0", corner_radius=10)
    button_area_br.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=10)
    # Cấu hình grid cho khu vực nút (để các nút xếp chồng lên nhau và giãn nở)
    button_area_br.grid_columnconfigure(0, weight=1)
    # Nút Mượn Sách
    btn_borrow = ctk.CTkButton(button_area_br, 
                            text="📥 Mượn Sách", 
                            fg_color="#4CAF50", 
                            hover_color="#388E3C")
    btn_borrow.grid(row=0, column=0, pady=(50, 10), padx=20, sticky="ew")
    # Nút Trả Sách
    btn_return = ctk.CTkButton(button_area_br,
                            text="📤 Trả Sách", 
                            fg_color="#F44336", 
                            hover_color="#D32F2F")  
    btn_return.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
    # Nút Tra cứu
    btn_search_br = ctk.CTkButton(button_area_br, 
                            text="🔍 Tra cứu", 
                            fg_color="#3C8EFA", 
                            hover_color="#5AA0FF")
    btn_search_br.grid(row=2, column=0, pady=(10, 50), padx=20, sticky="ew")

    #========================================================
    # === HÀNG 1 CỘT 3: Khu Vực Thêm Sách MƯỢN             ==
    #========================================================
    book_form = ctk.CTkFrame(borrow_return_frame, fg_color="#FFFFFF", corner_radius=10)
    book_form.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
    book_form .grid_columnconfigure(0, weight=0) # Cột Label 1 (Không giãn nở)
    book_form .grid_columnconfigure(1, weight=1) # Cột Entry 1 (Giãn nở)
    ctk.CTkLabel(book_form , text="THÔNG TIN SÁCH MƯỢN", 
                font=ctk.CTkFont(size=16, weight="bold"), 
                text_color="#3C8EFA").grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
    # Mã sách
    ma_sach_label_br = ctk.CTkLabel(book_form , text="Mã sách:", font=ctk.CTkFont(size=13))
    ma_sach_label_br.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
    sach_options = ["Chọn mã sách", "AB12001", "AB12002", "AB12003"]
    entry_ma_sach_br = ctk.CTkComboBox(book_form , values=sach_options)
    entry_ma_sach_br.set(sach_options[0]) # Đặt giá trị mặc định là "Chọn mã sách"
    entry_ma_sach_br.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
    # Tên sách
    ten_sach_label_br = ctk.CTkLabel(book_form , text="Tên sách:", font=ctk.CTkFont(size=13))
    ten_sach_label_br.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ten_sach_br = ctk.CTkEntry(book_form , placeholder_text="Tên cuốn sách")
    entry_ten_sach_br.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
    

    #========================================================
    # === HÀNG 2: Khu vực Bảng Lịch sử/Đang mượn (Giãn nở) ==
    #========================================================
    list_area_br = ctk.CTkFrame(borrow_return_frame, fg_color="#FFFFFF", corner_radius=10)
    list_area_br.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=(0, 10))

    list_title_br = ctk.CTkLabel(list_area_br, text="LỊCH SỬ GIAO DỊCH / SÁCH ĐANG ĐƯỢC MƯỢN", 
                                font=ctk.CTkFont(size=14, weight="bold"), text_color="#3C8EFA")
    list_title_br.pack(padx=20, pady=20)


    content_frames["Mượn trả sách"] = borrow_return_frame # Lưu Frame

    
#============================================================================================================================================ 
    # -- 5. Tạo Frame Thống kê Báo cáo ---
#============================================================================================================================================ 
    statistics_frame = ctk.CTkFrame(main_content_area)
    stats_label = ctk.CTkLabel(statistics_frame, text="THỐNG KÊ BÁO CÁO", font=ctk.CTkFont(size=30))
    stats_label.pack(expand=True)
    content_frames["Thống kê báo cáo"] = statistics_frame # Lưu Frame
#============================================================================================================================================ 
    # -- 6. Tạo Frame Cài đặt ---
#============================================================================================================================================     
    settings_frame = ctk.CTkFrame(main_content_area)
    settings_label = ctk.CTkLabel(settings_frame, text="CÀI ĐẶT ỨNG DỤNG", font=ctk.CTkFont(size=30))
    settings_label.pack(expand=True)
    content_frames["Cài đặt"] = settings_frame # Lưu Frame
    

    # --- Gán lệnh gọi hàm cho các nút Sidebar ---
    btn_mainMenu.configure(command=lambda btn=btn_mainMenu: switch_view("Trang chủ", btn))
    btn_bookManagement.configure(command=lambda btn=btn_bookManagement: switch_view("Quản lý sách", btn))
    btn_readerManagement.configure(command=lambda btn=btn_readerManagement: switch_view("Quản lý độc giả", btn))
    btn_borrowReturnManagement.configure(command=lambda btn=btn_borrowReturnManagement: switch_view("Mượn trả sách", btn))
    btn_statisticsReports.configure(command=lambda btn=btn_statisticsReports: switch_view("Thống kê báo cáo", btn))
    btn_settings.configure(command=lambda btn=btn_settings: switch_view("Cài đặt", btn))
    btn_logout.configure(command=lambda: messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất thành công!"))

    # --- THIẾT LẬP TRẠNG THÁI MẶC ĐỊNH KHI MỞ ---
    switch_view("Trang chủ", btn_mainMenu)

#==========================Chạy hàm giao diện================
    root.mainloop()

if __name__ == "__main__":
    OpenMainWindow()
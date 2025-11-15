#==========================Thư viện==========================
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from tkcalendar import DateEntry
from handlers.persistence_manager import *
from handlers.persistense_manager_2 import *
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
readeer_widget = {}

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
                               hover_color="#D32F2F",
                               command=lambda: delete_book(book_widget))
    btn_delete.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

    # Nút Tra cứu 
    btn_search = ctk.CTkButton(button_area_frame, 
                            text="🔍 Tra cứu", 
                            fg_color="#3C8EFA", 
                            hover_color="#5AA0FF",
                            command=lambda: search_book(book_widget))
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
    # ========================================================
    # ! BỔ SUNG: Tạo Context Menu (Menu chuột phải)
    # ========================================================   
    # 1. Tạo một Menu widget
    context_menu = tk.Menu(root, 
                           tearoff=0, 
                           bg="#FFFFFF", 
                           fg="#000000",
                           activebackground=ACTIVE_COLOR, 
                           activeforeground="#FFFFFF")
                           
    context_menu.add_command(label="✨ Làm mới Form (Clear)", 
                             command=lambda: clear_book_entries(book_widget))
    context_menu.add_command(label="🔄 Tải lại danh sách (Reload)", 
                             command=load_book_data) # Tải lại toàn bộ Treeview
    context_menu.add_separator()
    context_menu.add_command(label="Thoát menu")

    # 2. Tạo hàm để hiển thị menu tại vị trí chuột
    def show_context_menu(event):
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    # 3. Gán (Bind) sự kiện chuột phải (<Button-3>) cho các khu vực
    book_management_frame.bind("<Button-3>", show_context_menu)
    input_form_frame.bind("<Button-3>", show_context_menu)
    list_area_frame.bind("<Button-3>", show_context_menu)
    tree_view.bind("<Button-3>", show_context_menu)
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
    ma_doc_gia_label = ctk.CTkLabel(intput_reader_form_frame , text="Mã độc giả (7 Ký tự)*:", font=ctk.CTkFont(size=13))
    ma_doc_gia_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ma_doc_gia = ctk.CTkEntry(intput_reader_form_frame , placeholder_text="VD: DG0001")
    entry_ma_doc_gia.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="ew")
    # Họ tên 
    ho_ten_label = ctk.CTkLabel(intput_reader_form_frame , text="Họ tên*:", font=ctk.CTkFont(size=13))
    ho_ten_label.grid(row=0, column=2, padx=(20, 10), pady=10, sticky="w")
    entry_ho_ten = ctk.CTkEntry(intput_reader_form_frame , placeholder_text="Họ và tên độc giả")
    entry_ho_ten.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="ew")
    # Địa chỉ
    dia_chi_label = ctk.CTkLabel(intput_reader_form_frame , text="Địa chỉ*:", font=ctk.CTkFont(size=13))
    dia_chi_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_dia_chi = ctk.CTkEntry(intput_reader_form_frame , placeholder_text="Địa chỉ liên hệ")
    entry_dia_chi.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
    # Số điện thoại
    so_dien_thoai_label = ctk.CTkLabel(intput_reader_form_frame , text="Số điện thoại*:", font=ctk.CTkFont(size=13))
    so_dien_thoai_label.grid(row=1, column=2, padx=(20, 10), pady=10, sticky="w")
    entry_so_dien_thoai = ctk.CTkEntry(intput_reader_form_frame , placeholder_text="Số điện thoại liên hệ")
    entry_so_dien_thoai.grid(row=1, column=3, padx=(0, 20), pady=10, sticky="ew")
    #Ngay sỉnh 
    ngay_sinh_label = ctk.CTkLabel(intput_reader_form_frame , text="Ngày sinh*:", font=ctk.CTkFont(size=13))
    ngay_sinh_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ngay_sinh = DateEntry(intput_reader_form_frame , selexmode='day', date_pattern='dd/mm/yyyy',
                                width=18, background='white', foreground='black', borderwidth=1)
    entry_ngay_sinh.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")

    #lưu trữ widget độc giả
    readeer_widget = {
        'MaDocGia': entry_ma_doc_gia,
        'HoTen': entry_ho_ten,
        'DiaChi': entry_dia_chi,
        'SoDienThoai': entry_so_dien_thoai,
        'NgaySinh': entry_ngay_sinh
    }

    # Nút Thao tác
    reader_button_area_frame = ctk.CTkFrame(reader_management_frame, fg_color="#F0F0F0", corner_radius=10)
    reader_button_area_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=10)
    # Cấu hình grid cho khu vực nút (để các nút xếp chồng lên nhau và giãn nở)
    reader_button_area_frame.grid_columnconfigure(0, weight=1)
    # Nút Thêm
    btn_add_reader = ctk.CTkButton(reader_button_area_frame, 
                                   text=" ➕ Thêm Mới", 
                                   fg_color="#4CAF50", 
                                   hover_color="#388E3C",
                                   command=lambda: add_reader(readeer_widget))
    btn_add_reader.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")
    # Nút Sửa   
    btn_update_reader = ctk.CTkButton(reader_button_area_frame, 
                                      text="🔄 Cập nhật", 
                                      fg_color="#FFC107", 
                                      hover_color="#FFB300",
                                      command=lambda: update_reader(readeer_widget))
    btn_update_reader.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
    # Nút Xóa
    btn_delete_reader = ctk.CTkButton(reader_button_area_frame, 
                                      text="🗑️ Xóa Độc Giả", 
                                      fg_color="#F44336", 
                                      hover_color="#D32F2F",
                                      command=lambda: delete_reader(readeer_widget))   
    btn_delete_reader.grid(row=2, column=0, pady=10, padx=20, sticky="ew")
    # Nút Tra cứu
    btn_search_reader = ctk.CTkButton(reader_button_area_frame, 
                            text="🔍 Tra cứu", 
                            fg_color="#3C8EFA", 
                            hover_color="#5AA0FF",
                            command=lambda: search_reader(readeer_widget))
    btn_search_reader.grid(row=3, column=0, pady=(10, 20), padx=20, sticky="ew")
    
    # Khu vực List/Bảng (Giãn nở)
    reader_list_area_frame = ctk.CTkFrame(reader_management_frame, fg_color="#FFFFFF", corner_radius=10)
    # Đặt Frame list chiếm cả 2 cột
    reader_list_area_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
    # Ví dụ nội dung trong List
    reader_list_title = ctk.CTkLabel(reader_list_area_frame, text="DANH SÁCH CÁC ĐỘC GIẢ", 
                            font=ctk.CTkFont(size=14, weight="bold"), text_color="#3C8EFA") 
    reader_list_title.pack(padx=20, pady=20)
    reader_column = ("Mã độc giả", "Họ tên", "Địa chỉ", "Số điện thoại", "Ngày sinh")
    reader_tree_view = ttk.Treeview(reader_list_area_frame, columns=reader_column, show ="headings", height=10)
    for col in reader_column:
        reader_tree_view.heading(col, text=col)
        reader_tree_view.column(col, width=100, anchor="center")
    reader_tree_view.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    reader_scrollbar = ctk.CTkScrollbar(reader_list_area_frame, orientation="vertical", command=reader_tree_view.yview)
    reader_tree_view.configure(yscrollcommand=reader_scrollbar.set)
    reader_scrollbar.pack(side="right", fill="y", pady=(0, 20))
    register_reader_treeview(reader_tree_view)
    register_reader_entries(readeer_widget)
    load_reader_data()  # Tải dữ liệu độc giả vào Treeview khi khởi tạo giao diện
    reader_tree_view.bind("<<TreeviewSelect>>", on_reader_select)
    content_frames["Quản lý độc giả"] = reader_management_frame # Lưu Frame
# bổ sung: Tạo Context Menu (Menu chuột phải) cho độc giả
    # 1. Tạo một Menu widget
    reader_context_menu = tk.Menu(root, 
                           tearoff=0,
                            bg="#FFFFFF",
                            fg="#000000",
                            activebackground=ACTIVE_COLOR,
                            activeforeground="#FFFFFF")
    reader_context_menu.add_command(label="✨ Làm mới Form (Clear)",    
                                command=lambda: clear_reader_entries(readeer_widget))
    reader_context_menu.add_command(label="🔄 Tải lại danh sách (Reload)"
                                    , command=load_reader_data) # Tải lại toàn bộ Treeview
    reader_context_menu.add_separator()
    reader_context_menu.add_command(label="Thoát menu")
    # 2. Tạo hàm để hiển thị menu tại vị trí chuột
    def show_reader_context_menu(event):
        try:
            reader_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            reader_context_menu.grab_release()
    # 3. Gán (Bind) sự kiện chuột phải (<Button-3>) cho các khu vực
    reader_management_frame.bind("<Button-3>", show_reader_context_menu)
    intput_reader_form_frame .bind("<Button-3>", show_reader_context_menu)
    reader_list_area_frame.bind("<Button-3>", show_reader_context_menu)
    reader_tree_view.bind("<Button-3>", show_reader_context_menu)
    
#============================================================================================================================================ 
    # -- 4. Tạo Frame Mượn Trả Sách ---
#============================================================================================================================================ 
    ROOT_BG_COLOR = "#E1F4FD" 

    borrow_return_frame = ctk.CTkFrame(main_content_area, fg_color=ROOT_BG_COLOR) 

    # Cấu hình grid
    borrow_return_frame.grid_columnconfigure(0, weight=1) 
    borrow_return_frame.grid_columnconfigure(1, weight=0)
    borrow_return_frame.grid_columnconfigure(2, weight=1)
    borrow_return_frame.grid_rowconfigure(0, weight=0)
    borrow_return_frame.grid_rowconfigure(1, weight=0)
    borrow_return_frame.grid_rowconfigure(2, weight=1)
    
    #========================================================
    # === HÀNG 0: Tiêu đề Chung ===
    #========================================================
    frame_title_br = ctk.CTkLabel(borrow_return_frame, 
                                   text="QUẢN LÝ MƯỢN TRẢ SÁCH", 
                                   font=ctk.CTkFont(size=24, weight="bold"), 
                                   text_color="#3C8EFA")
    frame_title_br.grid(row=0, column=0, columnspan=3, padx=20, pady=(15, 10), sticky="w")
    
    #========================================================
    #=============HÀNG 1, CỘT 0: frame nhập phiếu============
    #========================================================
    input_borrow_frame = ctk.CTkFrame(borrow_return_frame, fg_color="#FFFFFF", corner_radius=10)   
    input_borrow_frame.grid(row=1, column=0, sticky="new", padx=10, pady=10)

    input_borrow_frame.grid_columnconfigure(0, weight=0)
    input_borrow_frame.grid_columnconfigure(1, weight=1)
    input_borrow_frame.grid_columnconfigure(2, weight=0)
    input_borrow_frame.grid_columnconfigure(3, weight=1)
    
    ctk.CTkLabel(input_borrow_frame, text="THÔNG TIN PHIẾU MƯỢN", 
                 font=ctk.CTkFont(size=16, weight="bold"), 
                 text_color="#3C8EFA").grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
    #Mã phiếu
    ma_phieu_label = ctk.CTkLabel(input_borrow_frame, text="Mã phiếu mượn*:", font=ctk.CTkFont(size=13))
    ma_phieu_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ma_phieu = ctk.CTkEntry(input_borrow_frame, placeholder_text="121125001")
    entry_ma_phieu.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
    #Mã độc giả
    ma_doc_gia_label_br = ctk.CTkLabel(input_borrow_frame, text="Mã độc giả:", font=ctk.CTkFont(size=13))
    ma_doc_gia_label_br.grid(row=1, column=2, padx=(20, 10), pady=10, sticky="w")
    doc_gia_options = ["Chọn mã DG"] 
    entry_ma_doc_gia_br = ctk.CTkComboBox(input_borrow_frame, values=doc_gia_options, 
                                          command=on_reader_id_select) # Đã thêm command
    entry_ma_doc_gia_br.set(doc_gia_options[0]) 
    entry_ma_doc_gia_br.grid(row=1, column=3, padx=(0, 20), pady=10, sticky="ew") 
    #Tên độc giả
    ten_doc_gia_label = ctk.CTkLabel(input_borrow_frame, text="Tên độc giả:", font=ctk.CTkFont(size=13))
    ten_doc_gia_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ten_doc_gia = ctk.CTkEntry(input_borrow_frame, placeholder_text="Tên độc giả (Hiển thị)", state='readonly') 
    entry_ten_doc_gia.grid(row=2, column=1, columnspan=3, padx=(0, 20), pady=10, sticky="ew")
    #Ngày mượn
    ngay_muon_label = ctk.CTkLabel(input_borrow_frame, text="Ngày mượn:", font=ctk.CTkFont(size=13))
    ngay_muon_label.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ngay_muon = DateEntry(input_borrow_frame, selectmode='day', date_pattern='dd/mm/yyyy',
                                 width=18, background='white', foreground='black', borderwidth=1)
    entry_ngay_muon.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")   
    #Ngày hẹn trả
    ngay_hen_tra_label = ctk.CTkLabel(input_borrow_frame, text="Ngày hẹn trả:", font=ctk.CTkFont(size=13))
    ngay_hen_tra_label.grid(row=3, column=2, padx=(20, 10), pady=10, sticky="w")
    entry_ngay_hen_tra = DateEntry(input_borrow_frame, selectmode='day', date_pattern='dd/mm/yyyy',
                                     width=18, background='white', foreground='black', borderwidth=1)
    entry_ngay_hen_tra.grid(row=3, column=3, padx=(0, 20), pady=10, sticky="ew")
    # Nút TRA CỨU
    btn_search_br = ctk.CTkButton(input_borrow_frame, 
                                   text="🔍 TRA CỨU PHIẾU", 
                                   fg_color="#3C8EFA", 
                                   hover_color="#5AA0FF",
                                   command=search_borrow_ticket) #! THÊM COMMAND
    btn_search_br.grid(row=4, column=0, columnspan=2, pady=(15, 10), padx=20, sticky="ew")

    # Nút HỦY
    btn_cancel = ctk.CTkButton(input_borrow_frame, 
                                text="❌ HỦY/LÀM MỚI", 
                                fg_color="#777777", 
                                hover_color="#555555",
                                command=clear_borrow_form) #! THÊM COMMAND
    btn_cancel.grid(row=4, column=2, columnspan=2, pady=(15, 10), padx=20, sticky="ew")

    #========================================================
    #=============HÀNG 1, CỘT 1: frame nút xử lý=============
    #========================================================
    button_area_br = ctk.CTkFrame(borrow_return_frame, fg_color="#F0F0F0", corner_radius=10)
    button_area_br.grid(row=1, column=1, sticky="new", padx=10, pady=10) 
    button_area_br.grid_columnconfigure(0, weight=1)
    
    # --- Nhóm nút MƯỢN SÁCH ---
    borrow_buttons_frame = ctk.CTkFrame(button_area_br, fg_color="transparent")
    borrow_buttons_frame.grid(row=0, column=0, pady=10, padx=5, sticky="ew")
    borrow_buttons_frame.grid_columnconfigure(0, weight=1)
    
    ctk.CTkLabel(borrow_buttons_frame, text="--- Mượn Sách ---", text_color="#555").grid(row=0, column=0, pady=(5,0))
    
    btn_add_detail = ctk.CTkButton(borrow_buttons_frame, 
                                     text="➕ THÊM SÁCH", 
                                     fg_color="#4CAF50", 
                                     hover_color="#388E3C",
                                     command=add_book_to_cart) #! THÊM COMMAND
    btn_add_detail.grid(row=1, column=0, pady=10, padx=5, sticky="ew")

    btn_delete_detail = ctk.CTkButton(borrow_buttons_frame, 
                                        text="➖ XÓA SÁCH", 
                                        fg_color="#F44336", 
                                        hover_color="#D32F2F",
                                        command=remove_book_from_cart) #! THÊM COMMAND
    btn_delete_detail.grid(row=2, column=0, pady=10, padx=5, sticky="ew")
    
    btn_save_borrow = ctk.CTkButton(borrow_buttons_frame, 
                                      text="💾 LƯU PHIẾU MƯỢN", 
                                      fg_color="#3C8EFA", 
                                      hover_color="#5AA0FF",
                                      command=save_borrow_ticket) #! THÊM COMMAND
    btn_save_borrow.grid(row=3, column=0, pady=(10, 0), padx=5, sticky="ew")

    # --- Nhóm nút TRẢ SÁCH ---
    return_buttons_frame = ctk.CTkFrame(button_area_br, fg_color="transparent")
    return_buttons_frame.grid(row=1, column=0, pady=10, padx=5, sticky="ew")
    return_buttons_frame.grid_columnconfigure(0, weight=1)
    
    ctk.CTkLabel(return_buttons_frame, text="--- Trả Sách ---", text_color="#555").grid(row=0, column=0)
    
    btn_update_return = ctk.CTkButton(return_buttons_frame,
                                       text="⬆️ CẬP NHẬT TRẢ", 
                                       fg_color="#FF4500", 
                                       hover_color="#CC3000",
                                       command=update_book_return) #! THÊM COMMAND
    btn_update_return.grid(row=1, column=0, pady=10, padx=5, sticky="ew")

    #========================================================
    #========HÀNG 1, CỘT 2: frame nhập chi tiết phiếu========
    #========================================================
    detail_tab_view = ctk.CTkTabview(borrow_return_frame,
                                     segmented_button_fg_color=SIDEBAR_BG,
                                     segmented_button_selected_color=ACTIVE_COLOR,
                                     segmented_button_unselected_color=SIDEBAR_BG)
    detail_tab_view.grid(row=1, column=2, sticky="new", padx=10, pady=10)

    # --- Tab 1: THÊM SÁCH MƯỢN ---
    tab_muon = detail_tab_view.add("Thêm Sách Mượn")
    tab_muon.grid_columnconfigure(0, weight=0)
    tab_muon.grid_columnconfigure(1, weight=1)
    
    #Mã sách
    ma_sach_label_br = ctk.CTkLabel(tab_muon, text="Mã sách:", font=ctk.CTkFont(size=13))
    ma_sach_label_br.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="w")
    sach_options = ["Chọn mã sách"]
    entry_ma_sach_br = ctk.CTkComboBox(tab_muon, values=sach_options, 
                                     command=on_book_id_select) # Đã thêm command
    entry_ma_sach_br.set(sach_options[0])
    entry_ma_sach_br.grid(row=1, column=1, padx=(0, 20), pady=(20, 10), sticky="ew")
    
    #Tên sách
    ten_sach_label_br = ctk.CTkLabel(tab_muon, text="Tên sách:", font=ctk.CTkFont(size=13))
    ten_sach_label_br.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_ten_sach_br = ctk.CTkEntry(tab_muon, placeholder_text="Tên cuốn sách (Hiển thị)", state='readonly') 
    entry_ten_sach_br.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
    
    #Số lượng
    sl_sach_label_br = ctk.CTkLabel(tab_muon, text="Số lượng:", font=ctk.CTkFont(size=13))
    sl_sach_label_br.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_so_luong_br = ctk.CTkEntry(tab_muon, placeholder_text="Số lượng muốn mượn")
    entry_so_luong_br.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")

    # --- Tab 2: XỬ LÝ TRẢ SÁCH ---
    tab_tra = detail_tab_view.add("Xử Lý Trả Sách")
    tab_tra.grid_columnconfigure(0, weight=0)
    tab_tra.grid_columnconfigure(1, weight=1)
    
    #Ngày trả
    ngay_tra_tt_label = ctk.CTkLabel(tab_tra, text="Ngày trả TT:", font=ctk.CTkFont(size=13))
    ngay_tra_tt_label.grid(row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="w")
    entry_ngay_tra_tt = DateEntry(tab_tra, selectmode='day', date_pattern='dd/mm/yyyy',
                                  width=18, background='white', foreground='black', borderwidth=1)
    entry_ngay_tra_tt.grid(row=1, column=1, padx=(0, 20), pady=(20, 10), sticky="ew")
    
    #Tình trạng sách
    tinh_trang_label = ctk.CTkLabel(tab_tra, text="Tình trạng:", font=ctk.CTkFont(size=13))
    tinh_trang_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
    tinh_trang_options = ["Tốt", "Hư hỏng nhẹ", "Mất/Hỏng nặng"]
    combo_tinh_trang = ctk.CTkComboBox(tab_tra, values=tinh_trang_options)
    combo_tinh_trang.set("Tốt")
    combo_tinh_trang.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
    
    #Phí phạt
    phi_phat_label = ctk.CTkLabel(tab_tra, text="Phí phạt:", font=ctk.CTkFont(size=13))
    phi_phat_label.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="w")
    entry_phi_phat = ctk.CTkEntry(tab_tra, placeholder_text="0 (VNĐ)")
    entry_phi_phat.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")


    #========================================================
    #=========HÀNG 2: frame hiển thị danh sách phiếu=========
    #========================================================
    list_area_br = ctk.CTkFrame(borrow_return_frame, fg_color="#FFFFFF", corner_radius=10)
    list_area_br.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=(0, 10))
    # Cấu hình grid cho list_area_br
    list_area_br.grid_columnconfigure(0, weight=1) # Cột 0 cho Treeview Phiếu
    list_area_br.grid_columnconfigure(1, weight=1) # Cột 1 cho Treeview Chi Tiết
    list_area_br.grid_rowconfigure(1, weight=1) # Hàng 1 cho 2 Treeview
    
    list_title_br = ctk.CTkLabel(list_area_br, 
                                   text="DANH SÁCH PHIẾU VÀ CHI TIẾT", 
                                   font=ctk.CTkFont(size=16, weight="bold"), text_color="#3C8EFA")
    list_title_br.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")

    # --- Container cho 2 bảng ---
    list_container = ctk.CTkFrame(list_area_br, fg_color="transparent")
    list_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
    list_container.grid_columnconfigure(0, weight=1) # Bảng Phiếu Mượn
    list_container.grid_columnconfigure(1, weight=1) # Bảng Chi Tiết
    list_container.grid_rowconfigure(0, weight=1) # Hàng cho 2 frame

    # --- Bảng 1: Danh sách Phiếu Mượn (Master) ---
    phieu_muon_frame = ctk.CTkFrame(list_container, fg_color="transparent")
    phieu_muon_frame.grid(row=0, column=0, sticky="nsew", padx=(10,5), pady=(0,10))
    
    #! THÊM CẤU HÌNH GRID CHO SCROLLBAR
    phieu_muon_frame.grid_rowconfigure(1, weight=1)
    phieu_muon_frame.grid_columnconfigure(0, weight=1)
    
    ctk.CTkLabel(phieu_muon_frame, text="Danh Sách Phiếu Mượn (Click để xem chi tiết)", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5, sticky="w")
    
    phieu_muon_config = {
        "ma_phieu": ("Mã Phiếu", 100, ctk.CENTER),
        "ma_doc_gia": ("Mã Độc giả", 100, ctk.CENTER),
        "ten_doc_gia": ("Tên Độc giả", 150, ctk.W),
        "ngay_muon": ("Ngày Mượn", 100, ctk.CENTER),
        "ngay_tra_dk": ("Hạn Trả", 100, ctk.CENTER),
        "trang_thai": ("Trạng Thái", 120, ctk.CENTER)
    }
    phieu_muon_cols = tuple(phieu_muon_config.keys())
    phieu_muon_treeview = ttk.Treeview(phieu_muon_frame, columns=phieu_muon_cols, show="headings", height=10, selectmode="browse")
    for col_id, (text, width, anchor) in phieu_muon_config.items():
        phieu_muon_treeview.heading(col_id, text=text)
        phieu_muon_treeview.column(col_id, width=width, anchor=anchor)
    
    #! THÊM SCROLLBAR NGANG VÀ DỌC
    pm_scrollbar_y = ctk.CTkScrollbar(phieu_muon_frame, orientation="vertical", command=phieu_muon_treeview.yview, width= 13)
    pm_scrollbar_x = ctk.CTkScrollbar(phieu_muon_frame, orientation="horizontal", command=phieu_muon_treeview.xview, height= 13)
    phieu_muon_treeview.configure(yscrollcommand=pm_scrollbar_y.set, xscrollcommand=pm_scrollbar_x.set)

    #! ĐẶT VÀO GRID
    phieu_muon_treeview.grid(row=1, column=0, sticky="nsew")
    pm_scrollbar_y.grid(row=1, column=1, sticky="ns")
    pm_scrollbar_x.grid(row=2, column=0, sticky="ew") # Ngang
    
    # --- Bảng 2: Chi Tiết Sách Mượn (Detail / Giỏ hàng) ---
    chi_tiet_frame = ctk.CTkFrame(list_container, fg_color="transparent")
    chi_tiet_frame.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=(0,10))
    
    #! THÊM CẤU HÌNH GRID CHO SCROLLBAR
    chi_tiet_frame.grid_rowconfigure(1, weight=1)
    chi_tiet_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(chi_tiet_frame, text="Chi Tiết Sách Mượn", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

    chi_tiet_config = {
        "ma_sach": ("Mã Sách", 80, ctk.W),
        "ten_sach": ("Tên Sách", 150, ctk.W),
        "so_luong": ("SL", 40, ctk.CENTER),
        "ngay_tra_tt": ("Ngày Trả TT", 100, ctk.CENTER),
        "tinh_trang": ("Tình Trạng", 100, ctk.W),
        "phi_phat": ("Phí Phạt", 80, ctk.E)
    }
    chi_tiet_cols = tuple(chi_tiet_config.keys())
    chi_tiet_treeview = ttk.Treeview(chi_tiet_frame, columns=chi_tiet_cols, show="headings", height=10, selectmode="browse")
    for col_id, (text, width, anchor) in chi_tiet_config.items():
        chi_tiet_treeview.heading(col_id, text=text)
        chi_tiet_treeview.column(col_id, width=width, anchor=anchor)
    
    #! THÊM SCROLLBAR NGANG VÀ DỌC
    ct_scrollbar_y = ctk.CTkScrollbar(chi_tiet_frame, orientation="vertical", command=chi_tiet_treeview.yview, width= 13)
    ct_scrollbar_x = ctk.CTkScrollbar(chi_tiet_frame, orientation="horizontal", command=chi_tiet_treeview.xview, height= 13)
    chi_tiet_treeview.configure(yscrollcommand=ct_scrollbar_y.set, xscrollcommand=ct_scrollbar_x.set)

    #! ĐẶT VÀO GRID
    chi_tiet_treeview.grid(row=1, column=0, sticky="nsew")
    ct_scrollbar_y.grid(row=1, column=1, sticky="ns")
    ct_scrollbar_x.grid(row=2, column=0, sticky="ew") # Ngang

    #=============================================================================
    # KHỐI KẾT NỐI SỰ KIỆN (ĐÃ CẬP NHẬT)
    #=============================================================================
    borrow_widgets_dict = {
        # Frame Phiếu
        "reader_combo": entry_ma_doc_gia_br,
        "reader_name": entry_ten_doc_gia,
        "ma_phieu": entry_ma_phieu,
        "ngay_muon": entry_ngay_muon,
        "ngay_hen_tra": entry_ngay_hen_tra,
        
        # Tab Thêm Sách
        "book_combo": entry_ma_sach_br,
        "book_name": entry_ten_sach_br,
        "so_luong": entry_so_luong_br,
        
        # Tab Trả Sách
        "ngay_tra_tt": entry_ngay_tra_tt,
        "tinh_trang": combo_tinh_trang,
        "phi_phat": entry_phi_phat,
        
        # Treeviews
        "phieu_muon_tree": phieu_muon_treeview,
        "cart_tree": chi_tiet_treeview,
        
        # Tab View (để chuyển tab)
        "tab_view": detail_tab_view
    }
    register_borrow_widgets(borrow_widgets_dict)
    
    # Tải dữ liệu
    load_reader_ids_to_combobox()
    load_book_ids_to_combobox()
    load_borrow_list() 
    
    #! BỔ SUNG: Gán sự kiện click cho 2 Treeview
    phieu_muon_treeview.bind("<<TreeviewSelect>>", on_phieu_muon_select)
    chi_tiet_treeview.bind("<<TreeviewSelect>>", on_chi_tiet_select)
    
    content_frames["Mượn trả sách"] = borrow_return_frame # Lưu Frame

#============================================================================================================================================ 
    # -- 5. Tạo Frame Thống kê Báo cáo ---
#============================================================================================================================================ 
    ROOT_BG_COLOR = "#E1F4FD" 

    statistics_frame = ctk.CTkFrame(main_content_area, fg_color=ROOT_BG_COLOR)
    statistics_frame.grid_columnconfigure(0, weight=1) # Chỉ 1 cột chính
    statistics_frame.grid_rowconfigure(0, weight=0) # Hàng 0: Tiêu đề
    statistics_frame.grid_rowconfigure(1, weight=0) # Hàng 1: Bộ lọc/Điều khiển
    statistics_frame.grid_rowconfigure(2, weight=1) # Hàng 2: Biểu đồ/Bảng (GIÃN NỞ)

    #========================================================
    # === HÀNG 0: Tiêu đề Chung ===
    #========================================================
    frame_title_stats = ctk.CTkLabel(statistics_frame, 
                                    text="BẢNG ĐIỀU KHIỂN & BÁO CÁO THỐNG KÊ", 
                                    font=ctk.CTkFont(size=24, weight="bold"), 
                                    text_color="#3C8EFA")
    frame_title_stats.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")


    # === HÀNG 1: Khu vực Lựa chọn Báo cáo (Control Panel) ===
    control_panel_frame = ctk.CTkFrame(statistics_frame, fg_color="#FFFFFF", corner_radius=10)
    control_panel_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
    control_panel_frame.grid_columnconfigure((0, 2), weight=0) # Labels
    control_panel_frame.grid_columnconfigure((1, 3), weight=1) # Entries (giãn nở tốt)
    control_panel_frame.grid_columnconfigure((4, 6), weight=0) # Labels Từ/Đến
    control_panel_frame.grid_columnconfigure((5, 7), weight=1) # DateEntries (Giãn nở vừa phải)
    control_panel_frame.grid_columnconfigure((8, 9), weight=1) # Nút (Sử dụng columnspan)

    DATE_STYLE = {'date_pattern': 'dd/mm/yyyy', 'selectmode': 'day', 'width': 12, 'background': 'white', 'foreground': 'black', 'borderwidth': 1}

    # ----------------------------------------------------
    # --- HÀNG 0: Loại Báo cáo và Top N (Bộ lọc chính) ---
    # ----------------------------------------------------

    # 1. Lựa chọn Loại Báo cáo
    ctk.CTkLabel(control_panel_frame, text="Loại Báo cáo:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")
    combo_report_type = ctk.CTkComboBox(control_panel_frame, 
                                        values=["Top sách được mượn nhiều nhất", 
                                                "Top độc giả mượn nhiều sách nhất", 
                                                "Top sách có số lượng tồn nhiều nhất",
                                                "Top sách được mượn ít nhất", 
                                                "Top độc giả mượn ít sách nhất", 
                                                "Top sách có số lượng tồn ít nhất"])
    combo_report_type.grid(row=0, column=1, padx=(5, 15), pady=10, sticky="ew")

    # 2. Giá trị N
    ctk.CTkLabel(control_panel_frame, text="Top N:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(15, 5), pady=10, sticky="w")
    entry_top_n = ctk.CTkEntry(control_panel_frame, placeholder_text="VD: 5")
    entry_top_n.grid(row=0, column=3, padx=(5, 15), pady=10, sticky="ew")
    entry_top_n.insert(0, "10") 

    # ----------------------------------------------------
    # --- HÀNG 1: Phạm vi Ngày tháng và Nút Thao tác ---
    # ----------------------------------------------------

    # 3. Lựa chọn Phạm vi Thời gian (DateEntry)
    ctk.CTkLabel(control_panel_frame, text="Từ Ngày:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=(15, 5), pady=(0, 15), sticky="w")
    entry_date_from = DateEntry(control_panel_frame, **DATE_STYLE)
    entry_date_from.grid(row=1, column=1, padx=(5, 15), pady=(0, 15), sticky="ew")

    ctk.CTkLabel(control_panel_frame, text="Đến Ngày:", font=ctk.CTkFont(size=13)).grid(row=1, column=2, padx=(15, 5), pady=(0, 15), sticky="w")
    entry_date_to = DateEntry(control_panel_frame, **DATE_STYLE)
    entry_date_to.grid(row=1, column=3, padx=(5, 15), pady=(0, 15), sticky="ew")


    # 4. Nút Xem Báo cáo
    btn_view_report = ctk.CTkButton(control_panel_frame, text="🔍 Xem Báo cáo", fg_color="#3C8EFA", hover_color="#5AA0FF",
                                    command=lambda: generate_report_and_chart(combo_report_type.get(), entry_top_n.get(), entry_date_from.get(), entry_date_to.get(), display_report_frame))
    btn_view_report.grid(row=0, column=7, padx=(5, 15), pady=(0, 15), sticky="ew") 

    # 5. Nút Xuất Excel
    btn_export_excel = ctk.CTkButton(control_panel_frame, text="📄 Xuất Excel", fg_color="#4CAF50", hover_color="#388E3C",
                                    command=lambda: export_data_to_excel(combo_report_type.get(), entry_top_n.get(), entry_date_from.get(), entry_date_to.get()))
    btn_export_excel.grid(row=1, column=7, padx=(5, 15), pady=(0, 15), sticky="ew")

    #========================================================
    # === HÀNG 2: Khu vực Biểu đồ/Bảng dữ liệu (Giãn nở) ===
    #========================================================
    display_report_frame = ctk.CTkFrame(statistics_frame, fg_color="#FFFFFF", corner_radius=10)
    display_report_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))

    # Khu vực này sẽ là nơi bạn nhúng biểu đồ Matplotlib hoặc Treeview kết quả
    ctk.CTkLabel(display_report_frame, 
                text="KHU VỰC HIỂN THỊ BIỂU ĐỒ HOẶC BẢNG DỮ LIỆU KẾT QUẢ", 
                font=ctk.CTkFont(size=16, weight="bold")).pack(expand=True, padx=50, pady=50)


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
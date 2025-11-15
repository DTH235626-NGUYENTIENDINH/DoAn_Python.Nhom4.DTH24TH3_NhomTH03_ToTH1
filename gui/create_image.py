from PIL import Image
import os

# --- TÙY CHỈNH Ở ĐÂY ---
FRAME_WIDTH = 350
FRAME_HEIGHT = 480
OUTPUT_DIR = "Picture" # Thư mục bạn muốn lưu file vào
OUTPUT_NAME = "frame_bg.png" # Tên file
# Màu (R, G, B). (0, 0, 0) là ĐEN. (255, 255, 255) là TRẮNG.
COLOR = (255, 255, 255) 
# Độ mờ (0=trong suốt, 255=đặc). 128 là 50%.
ALPHA = 255
# -------------------------

def create_transparent_png():
    """
    Tạo một file PNG bán trong suốt với màu và độ trong suốt được chỉ định.
    """
    
    # Tạo ảnh mới với chế độ RGBA (Red, Green, Blue, Alpha)
    # (COLOR + (ALPHA,)) sẽ tạo ra (R, G, B, A)
    img = Image.new('RGBA', (FRAME_WIDTH, FRAME_HEIGHT), COLOR + (ALPHA,)) 
    
    # Đảm bảo thư mục "Picture" tồn tại
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Đã tạo thư mục: {OUTPUT_DIR}")
        
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    img.save(output_path)
    print(f"Đã tạo file PNG bán trong suốt thành công tại: {output_path}")

if __name__ == "__main__":
    create_transparent_png()
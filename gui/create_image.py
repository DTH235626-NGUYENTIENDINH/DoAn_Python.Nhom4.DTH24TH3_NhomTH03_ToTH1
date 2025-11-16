from PIL import Image
import os

# --- TÙY CHỈNH ---
FRAME_WIDTH = 350
FRAME_HEIGHT = 480
OUTPUT_DIR = "Picture" 
OUTPUT_NAME = "frame_bg.png" 
COLOR = (255, 255, 255) 
ALPHA = 255
# -------------------------

def create_transparent_png():
    """
    Tạo một file PNG bán trong suốt với màu và độ trong suốt được chỉ định.
    """
    
    # Tạo ảnh mới
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
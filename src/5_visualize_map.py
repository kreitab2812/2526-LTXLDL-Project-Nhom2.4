import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# --- CẤU HÌNH ---
RAW_PATH = 'raw'
PROCESSED_PATH = 'processed'
FIGURES_PATH = 'figures'

# TỌA ĐỘ BẢN ĐỒ (Lấy từ README của đề bài)
# Góc Tây Bắc (Top-Left): 42.3017 N, 93.5673 W
# Góc Đông Nam (Bottom-Right): 42.1609 N, 93.1923 W
# Lưu ý: Dữ liệu của Vastopolis dùng tọa độ dương cho độ Tây (West), 
# nên giá trị càng lớn thì càng về phía bên Trái (Tây).
MAP_OPTS = {
    'top_lat': 42.3017,
    'bottom_lat': 42.1609,
    'left_long': 93.5673,  # Max Longitude (West)
    'right_long': 93.1923  # Min Longitude (East)
}

def draw_infection_map():
    print("🗺️ Đang vẽ bản đồ lây lan dịch bệnh...")
    
    # 1. Đọc dữ liệu Mapping và Ảnh bản đồ
    map_file = os.path.join(RAW_PATH, 'Vastopolis_Map.png')
    data_file = os.path.join(PROCESSED_PATH, 'keyword_location_mapping_2.4.csv')
    
    if not os.path.exists(map_file):
        print(f"❌ Không tìm thấy ảnh bản đồ tại {map_file}. Hãy copy ảnh vào thư mục raw/")
        return

    try:
        img = mpimg.imread(map_file)
        df = pd.read_csv(data_file)
        
        # Chỉ lấy triệu chứng bệnh (Symptom)
        df = df[df['type'] == 'symptom']
        
        # Lấy Top 3 bệnh phổ biến nhất để vẽ màu khác nhau
        top_diseases = df['keyword'].value_counts().head(3).index.tolist()
        print(f"   -> Vẽ bản đồ cho 3 bệnh chính: {top_diseases}")

    except Exception as e:
        print(f"❌ Lỗi đọc dữ liệu: {e}")
        return

    # 2. Thiết lập vẽ
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Hiển thị ảnh nền bản đồ
    # extent=[left, right, bottom, top] theo hệ trục pixel hoặc tọa độ
    ax.imshow(img, extent=[MAP_OPTS['left_long'], MAP_OPTS['right_long'], 
                           MAP_OPTS['bottom_lat'], MAP_OPTS['top_lat']])

    # 3. Vẽ các điểm (Scatter Plot)
    # Vì trục X của ảnh là từ Trái qua Phải (West -> East), 
    # nhưng số liệu độ Tây lại giảm dần (93.5 -> 93.1).
    # Matplotlib sẽ tự xử lý trục nếu ta khai báo extent đúng ở trên.
    
    colors = ['red', 'blue', 'orange'] # Màu cho top 3 bệnh
    
    for i, disease in enumerate(top_diseases):
        subset = df[df['keyword'] == disease]
        ax.scatter(subset['long'], subset['lat'], 
                   c=colors[i], label=disease, 
                   s=10, alpha=0.6, edgecolors='white', linewidth=0.5)

    # Vẽ các bệnh còn lại (màu xám nhỏ hơn)
    others = df[~df['keyword'].isin(top_diseases)]
    ax.scatter(others['long'], others['lat'], 
               c='gray', label='others', 
               s=5, alpha=0.3)

    plt.title('Bản đồ phân bố dịch bệnh tại Vastopolis (Nhóm 2.4)')
    plt.legend(loc='upper right')
    plt.xlabel('Longitude (W)')
    plt.ylabel('Latitude (N)')
    
    # Lưu file
    out_path = os.path.join(FIGURES_PATH, 'vastopolis_infection_map.png')
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Đã lưu bản đồ vào: {out_path}")

if __name__ == "__main__":
    draw_infection_map()
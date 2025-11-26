import pandas as pd
import numpy as np
import os

# --- CẤU HÌNH ---
PROCESSED_PATH = 'processed'

def process_data():
    print("🚀 Bắt đầu giai đoạn 2: Làm sạch & Kết nối dữ liệu...")

    # 1. ĐỌC DỮ LIỆU TỪ
    try:
        df_mb = pd.read_csv(os.path.join(PROCESSED_PATH, 'microblog_2.4.csv'), parse_dates=['created_at'])
        df_weather = pd.read_csv(os.path.join(PROCESSED_PATH, 'weather_2.4.csv'), parse_dates=['date'])
        print(f"✅ Đã tải: {len(df_mb):,} blogs và {len(df_weather)} dòng thời tiết.")
    except Exception as e:
        print(f"❌ Lỗi không tìm thấy file processed: {e}")
        return

    # 2. XỬ LÝ MICROBLOGS (Text & Location)
    print("🛠 Đang xử lý Text và Location...")
    
    # 2.1 Chuẩn hóa Text: Chuyển về chữ thường (lowercase)
    df_mb['text_clean'] = df_mb['text'].astype(str).str.lower().str.strip()

    # 2.2 Tách Tọa độ (Location)
    # Định dạng trong file thường là "Lat Long" cách nhau bởi khoảng trắng
    try:
        # Tách cột Location thành 2 cột tạm
        loc_split = df_mb['location'].astype(str).str.split(expand=True)
        
        # Gán vào dataframe chính (chuyển sang float để tính toán)
        df_mb['lat'] = pd.to_numeric(loc_split[0], errors='coerce')
        df_mb['long'] = pd.to_numeric(loc_split[1], errors='coerce')
        
        # Loại bỏ những dòng không có tọa độ chuẩn
        df_mb = df_mb.dropna(subset=['lat', 'long'])
        print(f"   -> Sau khi lọc tọa độ lỗi, còn lại: {len(df_mb):,} dòng")
        
    except Exception as e:
        print(f"⚠️ Cảnh báo lỗi tách tọa độ: {e}")

    # 3. XỬ LÝ THỜI TIẾT (Upsampling & Merge)
    print("☁️ Đang kết nối dữ liệu Thời tiết...")
    
    # Tạo cột ngày (chỉ lấy phần ngày, bỏ giờ phút) cho microblog
    df_mb['date_only'] = df_mb['created_at'].dt.floor('D')
    
    # Đổi tên cột date trong weather thành date_only để merge
    df_weather['date_only'] = df_weather['date']

    # Thực hiện Merge (Left Join): Giữ lại toàn bộ Blog, ghép thông tin thời tiết vào
    df_merged = pd.merge(
        df_mb, 
        df_weather[['date_only', 'weather', 'wind_direction', 'average_wind_speed']], 
        on='date_only', 
        how='left'
    )

    # 4. LƯU KẾT QUẢ
    output_file = os.path.join(PROCESSED_PATH, 'microblog_merged_2.4.csv')
    
    # Chỉ giữ lại các cột cần thiết cho nhẹ
    cols_to_keep = [
        'id', 'created_at', 'lat', 'long', 'text_clean', 
        'weather', 'wind_direction', 'average_wind_speed'
    ]
    
    df_merged[cols_to_keep].to_csv(output_file, index=False, encoding='utf-8')
    
    print("-" * 30)
    print(f"✅ HOÀN THÀNH! File đã lưu tại: {output_file}")
    print("Dữ liệu mẫu 5 dòng đầu:")
    print(df_merged[cols_to_keep].head().to_string())

if __name__ == "__main__":
    process_data()
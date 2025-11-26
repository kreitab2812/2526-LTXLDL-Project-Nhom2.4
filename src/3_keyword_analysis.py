import pandas as pd
import os
import re

# --- CẤU HÌNH ---
RAW_PATH = 'raw'
PROCESSED_PATH = 'processed'
INPUT_FILE = 'microblog_merged_2.4.csv'
SYMPTOMS_LIST = {
    'flu', 'fever', 'stomach', 'ache', 'chill', 'medicine', 'sick', 
    'pain', 'virus', 'cough', 'nausea', 'vomit', 'diarrhea', 'headache',
    'throat', 'sneeze', 'cold', 'infection', 'doctor', 'hospital'
}

def load_keywords():
    """Đọc file keywords.csv và phân loại"""
    print("📋 Đang đọc danh sách từ khóa...")
    kw_path = os.path.join(RAW_PATH, 'keywords.csv') # Hoặc keywords.txt tùy file
    
    if not os.path.exists(kw_path):
        print(f"❌ Không tìm thấy {kw_path}. Đang dùng danh sách mặc định.")
        return list(SYMPTOMS_LIST)

    try:
        df_kw = pd.read_csv(kw_path, header=None, names=['keyword'])
        # Làm sạch từ khóa
        keywords = df_kw['keyword'].astype(str).str.lower().str.strip().unique().tolist()
        print(f"✅ Đã tải {len(keywords)} từ khóa từ file.")
        return keywords
    except Exception as e:
        print(f"⚠️ Lỗi đọc file keywords: {e}. Dùng danh sách mặc định.")
        return list(SYMPTOMS_LIST)

def analyze_keywords():
    # 1. Load dữ liệu đã merge ở bước 2
    print("🚀 Bắt đầu phân tích từ khóa...")
    df = pd.read_csv(os.path.join(PROCESSED_PATH, INPUT_FILE), parse_dates=['created_at'])
    df['text_clean'] = df['text_clean'].fillna('') # Xử lý dòng trống
    
    # 2. Load danh sách từ khóa
    all_keywords = load_keywords()
    
    # 3. Quét từ khóa trong Text
    # Kỹ thuật: "Explode" dữ liệu. Một blog có thể chứa nhiều từ khóa.
    
    print("🔍 Đang quét từ khóa trong nội dung (Bước này hơi lâu chút)...")
    
    # Hàm tìm từ khóa trong 1 dòng text
    def find_keywords(text):
        found = []
        # Cách đơn giản: check string contains (có thể tối ưu bằng regex nếu dữ liệu quá lớn)
        for k in all_keywords:
            # Dùng \b để bắt chính xác từ (ví dụ tránh bắt 'flu' trong 'flutter')
            if pd.notna(text) and k in text: 
                found.append(k)
        return found

    df['found_keywords'] = df['text_clean'].apply(find_keywords)
    
    # 4. Tách dòng (Explode): Biến danh sách từ khóa thành từng dòng riêng biệt
    df_exploded = df.explode('found_keywords')
    
    # Bỏ những dòng không tìm thấy từ khóa nào (NaN)
    df_mapped = df_exploded.dropna(subset=['found_keywords']).copy()
    
    # Đổi tên cột cho chuẩn đề bài
    df_mapped.rename(columns={'found_keywords': 'keyword'}, inplace=True)
    
    # 5. Phân loại từ khóa (Symptom vs Other)
    df_mapped['type'] = df_mapped['keyword'].apply(
        lambda x: 'symptom' if x in SYMPTOMS_LIST else 'other'
    )
    
    print(f"✅ Tìm thấy tổng cộng {len(df_mapped):,} lượt xuất hiện từ khóa.")
    
    # 6. LƯU CÁC FILE KẾT QUẢ (Theo yêu cầu đề bài)
    
    # File 1: Bảng mapping chi tiết (Dùng để vẽ bản đồ Task 4)
    # Cần: location (lat, long), keyword, time
    out_map = os.path.join(PROCESSED_PATH, 'keyword_location_mapping_2.4.csv')
    cols_map = ['created_at', 'lat', 'long', 'keyword', 'type']
    df_mapped[cols_map].to_csv(out_map, index=False)
    print(f"💾 [1/2] Đã lưu file mapping vị trí: {out_map}")
    
    # File 2: Thống kê theo giờ (Dùng vẽ biểu đồ cột/đường Task 4)
    # Group by: Giờ + Keyword
    df_mapped['hour_str'] = df_mapped['created_at'].dt.strftime('%Y-%m-%d %H:00')
    
    stat_hourly = df_mapped.groupby(['hour_str', 'keyword', 'type', 'weather', 'wind_direction']).size().reset_index(name='count')
    
    out_stat = os.path.join(PROCESSED_PATH, 'stat_hourly_2.4.csv')
    stat_hourly.to_csv(out_stat, index=False)
    print(f"💾 [2/2] Đã lưu file thống kê theo giờ: {out_stat}")
    
    # Bonus: In thử top từ khóa triệu chứng xuất hiện nhiều nhất
    print("\n--- TOP 10 TRIỆU CHỨNG BỆNH PHỔ BIẾN NHẤT (NHÓM 2.4) ---")
    top_symptoms = df_mapped[df_mapped['type']=='symptom']['keyword'].value_counts().head(10)
    print(top_symptoms)

if __name__ == "__main__":
    analyze_keywords()
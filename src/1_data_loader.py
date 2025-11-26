import pandas as pd
import os

# --- CẤU HÌNH CHO NHÓM 2.4 ---
RAW_PATH = 'raw'
PROCESSED_PATH = 'processed'
START_DATE = '2011-05-12' # Ngày bắt đầu nhóm 2.4
END_DATE = '2011-05-15'   # Ngày kết thúc nhóm 2.4

def load_and_filter_microblogs():
    print("--- Đang xử lý Microblogs ---")
    file_path = os.path.join(RAW_PATH, 'Microblogs.csv')
    
    if not os.path.exists(file_path):
        # Fallback tìm tên thường
        file_path = os.path.join(RAW_PATH, 'microblogs.csv')
        if not os.path.exists(file_path):
            print(f"❌ Lỗi: Không tìm thấy file {file_path}")
            return

    try:
        # Đọc toàn bộ dưới dạng chuỗi (dtype=str) để tránh lỗi parse ngay từ đầu
        df = pd.read_csv(file_path, encoding='latin-1', dtype=str)
        
        # Chuẩn hóa tên cột
        df.columns = df.columns.str.lower().str.strip()
        
        # Chuyển đổi thời gian với errors='coerce'
        # errors='coerce' sẽ biến các giá trị lỗi thành NaT
        print("⏳ Đang chuyển đổi dữ liệu thời gian (sẽ mất vài giây)...")
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        
        # Kiểm tra xem có bao nhiêu dòng bị lỗi
        n_errors = df['created_at'].isna().sum()
        if n_errors > 0:
            print(f"⚠️ Cảnh báo: Phát hiện {n_errors} dòng có lỗi định dạng thời gian -> Đã loại bỏ.")
            df = df.dropna(subset=['created_at'])
        
        print(f"✅ Đã đọc xong. Tổng số dòng hợp lệ: {len(df):,}")

    except Exception as e:
        print(f"❌ Lỗi đọc file nghiêm trọng: {e}")
        return

    # Lọc dữ liệu theo ngày (Nhóm 2.4)
    mask = (df['created_at'] >= START_DATE) & (df['created_at'] < '2011-05-16')
    df_filtered = df.loc[mask].copy()
    
    print(f"✅ Đã lọc dữ liệu Nhóm 2.4 ({START_DATE} đến {END_DATE})")
    print(f"📊 Số dòng còn lại: {len(df_filtered):,}")

    # Lưu file
    out_file = os.path.join(PROCESSED_PATH, 'microblog_2.4.csv')
    df_filtered.to_csv(out_file, index=False, encoding='utf-8')
    print(f"💾 Đã lưu kết quả tại: {out_file}")

def load_and_filter_weather():
    print("\n--- Đang xử lý Weather ---")
    file_path = os.path.join(RAW_PATH, 'Weather.csv')
    
    if not os.path.exists(file_path):
        file_path = os.path.join(RAW_PATH, 'weather.csv')
        if not os.path.exists(file_path):
            print("❌ Không tìm thấy file Weather.csv")
            return

    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.lower().str.strip()
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            mask = (df['date'] >= START_DATE) & (df['date'] < '2011-05-16')
            df_filtered = df.loc[mask].copy()
            
            out_file = os.path.join(PROCESSED_PATH, 'weather_2.4.csv')
            df_filtered.to_csv(out_file, index=False, encoding='utf-8')
            # Vì dữ liệu thời tiết là theo ngày, nên 4 ngày = 4 dòng là CHÍNH XÁC.
            print(f"✅ Đã lọc và lưu Weather ({len(df_filtered)} dòng) vào {out_file}")
        else:
            print(f"❌ Không tìm thấy cột date. Các cột: {df.columns}")
        
    except Exception as e:
        print(f"❌ Lỗi xử lý Weather: {e}")

if __name__ == "__main__":
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    load_and_filter_microblogs()
    load_and_filter_weather()
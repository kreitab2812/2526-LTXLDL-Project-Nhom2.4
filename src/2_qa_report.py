import pandas as pd
import os

# --- CẤU HÌNH ---
RAW_PATH = 'raw'
REPORT_PATH = 'reports'
FILE_NAME = 'Microblogs.csv' # Tên file gốc (có chữ M hoa)

def check_data_quality():
    print("🕵️‍♂️ Đang chạy kiểm tra chất lượng dữ liệu (QA Rules)...")
    
    # Đường dẫn file
    file_path = os.path.join(RAW_PATH, FILE_NAME)
    if not os.path.exists(file_path):
        # Fallback: Thử tìm tên thường nếu tên hoa không thấy
        file_path = os.path.join(RAW_PATH, 'microblogs.csv')
    
    try:
        # 1. Đọc dữ liệu thô (đọc dạng string để bắt lỗi format)
        df = pd.read_csv(file_path, encoding='latin-1', dtype=str)
        
        # --- QUAN TRỌNG: CHUẨN HÓA TÊN CỘT VỀ CHỮ THƯỜNG ---
        df.columns = df.columns.str.lower().str.strip()
        
        total_rows = len(df)
        print(f"📊 Tổng số dòng dữ liệu thô: {total_rows:,}")
        
        qa_results = []

        # --- RULE 1: Kiểm tra lỗi định dạng thời gian (created_at) ---
        temp_dates = pd.to_datetime(df['created_at'], errors='coerce')
        invalid_dates = temp_dates.isna().sum()
        qa_results.append({
            'Rule': 'Check Date Format',
            'Description': 'Kiểm tra định dạng ngày tháng (YYYY-MM-DD HH:MM)',
            'Total_Errors': invalid_dates,
            'Error_Rate (%)': round((invalid_dates / total_rows) * 100, 4),
            'Action': 'Loại bỏ dòng lỗi (Drop)'
        })

        # --- RULE 2: Kiểm tra thiếu tọa độ (location) ---
        missing_loc = df['location'].isna().sum()
        qa_results.append({
            'Rule': 'Check Missing Location',
            'Description': 'Kiểm tra dòng thiếu thông tin vị trí',
            'Total_Errors': missing_loc,
            'Error_Rate (%)': round((missing_loc / total_rows) * 100, 4),
            'Action': 'Loại bỏ dòng lỗi (Drop)'
        })

        # --- RULE 3: Kiểm tra thiếu nội dung (text) ---
        missing_text = df['text'].isna().sum()
        qa_results.append({
            'Rule': 'Check Missing Text',
            'Description': 'Kiểm tra dòng không có nội dung blog',
            'Total_Errors': missing_text,
            'Error_Rate (%)': round((missing_text / total_rows) * 100, 4),
            'Action': 'Điền rỗng hoặc gắn cờ'
        })

        # --- RULE 4: Kiểm tra trùng lặp (Duplicate ID) ---
        # Kiểm tra cột id (đã lower)
        duplicate_ids = df.duplicated(subset=['id']).sum()
        qa_results.append({
            'Rule': 'Check Duplicates',
            'Description': 'Kiểm tra trùng lặp ID bài viết',
            'Total_Errors': duplicate_ids,
            'Error_Rate (%)': round((duplicate_ids / total_rows) * 100, 4),
            'Action': 'Giữ lại (Feature của dữ liệu)'
        })

        # --- XUẤT BÁO CÁO ---
        df_qa = pd.DataFrame(qa_results)
        
        # In ra màn hình
        print("\n📋 BẢNG TỔNG HỢP LỖI (QA SUMMARY):")
        print(df_qa.to_string(index=False))
        
        # Lưu ra file CSV theo yêu cầu đề bài
        os.makedirs(REPORT_PATH, exist_ok=True)
        out_file = os.path.join(REPORT_PATH, 'qa_summary.csv')
        df_qa.to_csv(out_file, index=False)
        print(f"\n✅ Đã lưu báo cáo QA vào: {out_file}")

    except Exception as e:
        print(f"❌ Lỗi khi chạy QA: {e}")

if __name__ == "__main__":
    check_data_quality()
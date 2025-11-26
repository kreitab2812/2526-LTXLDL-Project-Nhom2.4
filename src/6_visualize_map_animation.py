import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
import os

# --- CẤU HÌNH ---
RAW_PATH = 'raw'
PROCESSED_PATH = 'processed'
FIGURES_PATH = 'figures'

# Tọa độ bản đồ (Giữ nguyên như cũ)
MAP_OPTS = {
    'top_lat': 42.3017,
    'bottom_lat': 42.1609,
    'left_long': 93.5673,
    'right_long': 93.1923
}

def create_animation():
    print("🎬 Đang khởi tạo Animation (Máy quay chạy)...")
    
    # 1. Đọc dữ liệu & Ảnh nền
    map_file = os.path.join(RAW_PATH, 'Vastopolis_Map.png')
    data_file = os.path.join(PROCESSED_PATH, 'keyword_location_mapping_2.4.csv')
    
    if not os.path.exists(map_file):
        print("❌ Thiếu file ảnh bản đồ!")
        return

    # Đọc dữ liệu và convert thời gian
    df = pd.read_csv(data_file)
    df['created_at'] = pd.to_datetime(df['created_at'])
    
    # Chỉ lấy dữ liệu Triệu chứng bệnh
    df = df[df['type'] == 'symptom'].sort_values('created_at')
    
    # Tạo danh sách các khung giờ (Mỗi khung là 1 giờ)
    time_bins = pd.date_range(start=df['created_at'].min(), 
                              end=df['created_at'].max(), 
                              freq='1h')
    
    print(f"⏱ Tổng số khung hình (Frames): {len(time_bins)}")

    # 2. Thiết lập khung cảnh (Figure)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Load ảnh nền
    img = mpimg.imread(map_file)
    ax.imshow(img, extent=[MAP_OPTS['left_long'], MAP_OPTS['right_long'], 
                           MAP_OPTS['bottom_lat'], MAP_OPTS['top_lat']])
    
    ax.set_xlabel('Longitude (W)')
    ax.set_ylabel('Latitude (N)')
    
    # Khởi tạo Scatter plot rỗng
    scat = ax.scatter([], [], c='red', s=15, alpha=0.7, edgecolors='white', linewidth=0.5)
    
    # --- SỬA LỖI TẠI ĐÂY: Dùng ax.text thay vì ax.set_text ---
    title = ax.text(0.5, 1.05, "", transform=ax.transAxes, ha="center", fontsize=12, weight='bold')

    # 3. Hàm cập nhật từng khung hình
    def update(frame_idx):
        current_time = time_bins[frame_idx]
        
        # Lấy dữ liệu tích lũy
        current_data = df[df['created_at'] <= current_time]
        
        if not current_data.empty:
            offsets = current_data[['long', 'lat']].to_numpy()
            scat.set_offsets(offsets)
        
        # Cập nhật tiêu đề
        title.set_text(f"Diễn biến dịch bệnh: {current_time.strftime('%Y-%m-%d %H:%M')}")
        
        print(f"\r⏳ Đang render khung hình: {frame_idx + 1}/{len(time_bins)}", end="")
        
        return scat, title

    # 4. Tạo Animation
    ani = animation.FuncAnimation(fig, update, frames=len(time_bins), interval=150, blit=False)
    
    # 5. Lưu ra file GIF
    out_file = os.path.join(FIGURES_PATH, 'vastopolis_outbreak_timelapse.gif')
    print("\n💾 Đang lưu file GIF (Sẽ mất khoảng 10-30 giây)...")
    
    try:
        # Sử dụng PillowWriter
        writer = animation.PillowWriter(fps=5)
        ani.save(out_file, writer=writer)
        print("-" * 30)
        print(f"✅ XONG! Video đã lưu tại: {out_file}")
    except Exception as e:
        print(f"\n❌ Lỗi khi lưu GIF: {e}")

if __name__ == "__main__":
    create_animation()
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Cấu hình
PROCESSED_PATH = 'processed'
FIGURES_PATH = 'figures'

def draw_regional_wordclouds():
    print("☁️ Đang vẽ WordCloud theo từng khu vực...")
    df = pd.read_csv(os.path.join(PROCESSED_PATH, 'keyword_location_mapping_2.4.csv'))
    df_sym = df[df['type'] == 'symptom']

    # Định nghĩa biên giới khu vực DOWNTOWN (Khu trung tâm đông đúc nhất)
    # Dựa trên tọa độ bản đồ: Lat khoảng 42.2 - 42.25, Long khoảng 93.35 - 93.45
    # Lưu ý: Longitude là số dương trong dữ liệu này (theo cách ta xử lý)
    
    # Tách dữ liệu
    # Điều kiện này là ước lượng dựa trên bản đồ visual của bạn
    mask_downtown = (df_sym['lat'] < 42.25) & (df_sym['lat'] > 42.18) & \
                    (df_sym['long'] < 93.45) & (df_sym['long'] > 93.30)
    
    df_downtown = df_sym[mask_downtown]
    df_uptown = df_sym[~mask_downtown] # Các vùng còn lại (Uptown/Suburbia)

    print(f"   - Downtown: {len(df_downtown)} từ khóa")
    print(f"   - Uptown/Khác: {len(df_uptown)} từ khóa")

    # Hàm vẽ và lưu
    def save_wc(dataframe, title, filename):
        freq = dataframe.groupby('keyword')['keyword'].count().to_dict()
        if not freq: return
        wc = WordCloud(width=800, height=400, background_color='white', colormap='Reds').generate_from_frequencies(freq)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_PATH, filename))
        plt.close()
        print(f"✅ Đã lưu: {filename}")

    save_wc(df_downtown, 'WordCloud khu vực Downtown (Trung tâm)', 'wordcloud_downtown.png')
    save_wc(df_uptown, 'WordCloud khu vực Uptown & Ngoại ô', 'wordcloud_uptown.png')

if __name__ == "__main__":
    draw_regional_wordclouds()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# --- CẤU HÌNH ---
PROCESSED_PATH = 'processed'
FIGURES_PATH = 'figures'
INPUT_STAT = 'stat_hourly_2.4.csv'

def draw_charts():
    print("🎨 Đang vẽ các biểu đồ thống kê...")
    os.makedirs(FIGURES_PATH, exist_ok=True)
    
    # Đọc dữ liệu
    df = pd.read_csv(os.path.join(PROCESSED_PATH, INPUT_STAT))
    
    # Lọc chỉ lấy các từ khóa là Triệu chứng (Symptom) để vẽ cho đỡ rối
    df_sym = df[df['type'] == 'symptom'].copy()
    
    # 1. BIỂU ĐỒ CỘT: Top 10 triệu chứng phổ biến nhất
    print("   -> Vẽ biểu đồ 1: Top Symptoms...")
    top_symptoms = df_sym.groupby('keyword')['count'].sum().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_symptoms.values, y=top_symptoms.index, palette='viridis')
    plt.title('Top 10 Triệu chứng bệnh phổ biến (Nhóm 2.4)')
    plt.xlabel('Số lượt đề cập')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, 'top_symptoms_bar.png'))
    plt.close()

    # 2. BIỂU ĐỒ ĐƯỜNG: Diễn biến dịch bệnh theo thời gian
    print("   -> Vẽ biểu đồ 2: Time Series...")
    # Lấy top 5 bệnh để vẽ đường thôi cho dễ nhìn
    top_5_keys = top_symptoms.head(5).index.tolist()
    df_top5 = df_sym[df_sym['keyword'].isin(top_5_keys)]
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_top5, x='hour_str', y='count', hue='keyword', marker='o')
    plt.xticks(rotation=45, ha='right')
    plt.title('Xu hướng các triệu chứng chính theo giờ')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, 'symptom_trends_line.png'))
    plt.close()

    # 3. WORDCLOUD: Đám mây từ khóa
    print("   -> Vẽ biểu đồ 3: WordCloud...")
    # Tạo dict tần suất {từ: số lượng}
    freq_dict = df_sym.groupby('keyword')['count'].sum().to_dict()
    
    if freq_dict:
        wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_dict)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title('WordCloud các triệu chứng bệnh')
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_PATH, 'symptoms_wordcloud.png'))
        plt.close()
    
    print(f"✅ Đã lưu 3 biểu đồ vào thư mục {FIGURES_PATH}/")

if __name__ == "__main__":
    draw_charts()
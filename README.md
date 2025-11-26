# Vastopolis Epidemic Analysis - Group 2.4

Dự án phân tích dữ liệu dịch bệnh tại thành phố Vastopolis dựa trên dữ liệu Microblogs và Thời tiết (VAST Challenge 2011).

## 👥 Thành viên nhóm 2.4
1. Đinh Mạnh Cường 
2. Trịnh Minh Đức 
3. Dương Đức Minh

**Phạm vi dữ liệu:** 12/05/2011 - 15/05/2011

## 📊 Kết quả phân tích chính

### 1. Triệu chứng phổ biến
Dựa trên phân tích từ khóa, các triệu chứng xuất hiện nhiều nhất bao gồm:
- **Pain (Đau nhức):** 846 lượt
- **Sick (Ốm):** 717 lượt
- **Cold (Cảm lạnh):** 631 lượt
- **Flu (Cúm):** 496 lượt

![WordCloud](figures/symptoms_wordcloud.png)

### 2. Phân bố dịch bệnh
Dịch bệnh tập trung chủ yếu tại khu vực **Downtown** và **Uptown**, dọc theo dòng sông Vast River.

![Infection Map](figures/vastopolis_infection_map.png)

## 🛠 Hướng dẫn chạy lại (Reproduction)

### Yêu cầu
- Python 3.8+
- Các thư viện: `pandas`, `matplotlib`, `seaborn`, `wordcloud`

Cài đặt thư viện:
```bash
pip install -r requirements.txt
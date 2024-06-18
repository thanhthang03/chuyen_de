# Sử dụng hình ảnh Python chính thức làm nền tảng
FROM python:3.9

# Đặt thư mục làm việc trong container
WORKDIR /usr/src/app

# Sao chép tệp requirements.txt vào thư mục làm việc
COPY requirements.txt ./

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Chạy ứng dụng
CMD ["python", "chuyen_de.py"]

# Objective Detection and Tracker 

Dự án này cung cấp một giải pháp mạnh mẽ để phát hiện, theo dõi và đếm đối tượng trong video sử dụng mô hình YOLO và thuật toán ByteTrack. Hệ thống hỗ trợ nhiều chế độ đếm khác nhau như đếm theo dòng (Line), đếm theo vùng (Zone), và đếm theo làn đường (Lane/Multiple Lane).

## Tính năng chính

- **Phát hiện đối tượng:** Sử dụng YOLO (mặc định là `yolo26n.pt`) để phát hiện vật thể với độ chính xác cao.
- **Theo dõi đối tượng (Tracking):** Tích hợp ByteTrack để duy trì ID của đối tượng qua từng khung hình.
- **Đa dạng chế độ đếm:**
  - `line`: Đếm đối tượng khi đi ngang qua một vạch kẻ.
  - `zone`: Đếm đối tượng bên trong một vùng hình chữ nhật.
  - `lane_zone`: Đếm đối tượng trong một vùng đa giác tùy chỉnh (Polygon).
  - `multiple_lane_zone`: Đếm đồng thời trên nhiều làn đường với màu sắc phân biệt.
- **Cấu hình linh hoạt:** Mọi thông số từ mô hình, ngưỡng tin cậy (Confidence), đến các vùng đếm đều được cấu hình dễ dàng qua file YAML.
- **Lưu trữ kết quả:** Hỗ trợ lưu video đầu ra, hình ảnh từng frame và thông tin phát hiện.

## Cấu trúc thư mục

```text
Object-dection/
├── config/             # Cấu hình hệ thống (YAML)
├── core/               # Các module xử lý lõi (Load settings, Logging)
├── inputs/             # Dữ liệu đầu vào (Images, Videos)
├── models/             # Chứa các file trọng số mô hình (.pt)
├── outputs/            # Kết quả đầu ra (Videos, Logs)
├── scripts/            # Các script thử nghiệm và tiện ích
├── src/                # Mã nguồn chính của Pipeline
│   ├── counter/        # Logic đếm (Line, Zone, Lane)
│   ├── detector/       # Wrapper cho YOLO Detector
│   ├── saver/          # Logic lưu trữ kết quả
│   └── visualize/      # Công cụ vẽ và hiển thị
├── requirements.txt    # Danh sách thư viện cần thiết
└── run.py              # File chạy chính của dự án
```

## Hướng dẫn cài đặt

1. **Clone repository:**
   ```bash
   git clone https://github.com/nmc2004nd/Object-dection.git
   cd Object-dection
   ```

2. **Cài đặt môi trường:**
   Khuyến khích sử dụng Python 3.9+ và tạo môi trường ảo:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chuẩn bị mô hình:**
   Tải file trọng số YOLO (ví dụ `yolo26n.pt`) và đặt vào thư mục `models/`.

## Cách sử dụng

### 1. Cấu hình
Chỉnh sửa file `config/settings.yaml` để thiết lập các thông số:
- `detector`: Loại mô hình, ngưỡng `conf_threshold`, `iou_threshold`, và các `classes` cần phát hiện.
- `counter`: Chọn loại bộ đếm và định nghĩa các điểm (points) cho vùng đếm.
- `saver`: Bật/tắt chế độ lưu hình ảnh hoặc video.

### 2. Chạy chương trình
Chạy file `run.py` để bắt đầu quá trình xử lý:
```bash
python run.py
```

## Ví dụ cấu hình Counter (YAML)

**Đếm theo nhiều làn đường (Multiple Lane Zone):**
```yaml
counter:
  - type: multiple_lane_zone
    points: 
      - [[220, 55], [86, 285], [192, 285], [256, 55]]  # Vùng 1
      - [[192, 285], [256, 55], [294, 55], [315, 285]] # Vùng 2
    colors: [[0, 0, 255], [0, 255, 0]] # BGR format
    thickness: 2
```

## Yêu cầu hệ thống
- Python 3.8+
- OpenCV
- Ultralytics (YOLO)
- PyYAML



import cv2
import numpy as np


class ZoneCounter:
    def __init__(self, points: list[tuple]):
        self.points = points
        self.count = 0
        self.inside_id = set() # tránh trùng

    def update_count(self, detections: list[dict]):
        self.centers = []
        current_inside_id = set()

        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            track_id = detection['track_id']
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            self.centers.append((center_x, center_y))


            if self._inside_zone(center_x, center_y):
                current_inside_id.add(track_id)

        self.count = len(current_inside_id)


        self.inside_id = current_inside_id

    def _inside_zone(self, center_x: int, center_y: int) -> bool:
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        return x1 <= center_x <= x2 and y1 <= center_y <= y2
    
    def draw(self, frame):
        for cx, cy in self.centers:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        cv2.rectangle(frame, self.points[0], self.points[1], (0, 0, 255), 2)

        cv2.putText(frame, f'Count: {self.count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame
    
class LaneZoneCounter:
    def __init__(self, points: list[tuple], frame_size: tuple):
        self.frame_size = frame_size # (height, width)
        self.points = np.array(points, dtype=np.int32)
        self.count = 0
        self.counter_id = set() # tránh trùng ID đã đếm

        # Tạo mặt nạ cho khu vực được xác định bởi các điểm
        self.mask = np.zeros((frame_size[0], frame_size[1]), dtype=np.uint8)
        cv2.fillPoly(self.mask, [self.points], 255)

    def update_count(self, detections: list[dict]):
        self.centers = []
        current_inside_id = set()

        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            track_id = detection['track_id']
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)


            self.centers.append((center_x, center_y))

            if center_x < 0 or center_x >= self.frame_size[1] or center_y < 0 or center_y >= self.frame_size[0]:
                continue

            if self._inside_zone(center_x, center_y):
                current_inside_id.add(track_id)

            news = current_inside_id - self.counter_id # phần tử mới xuất hiện trong frame hiện tại
            self.counter_id.update(news) # cập nhật danh sách ID đã đếm
            if news:
                self.count += len(news)
        # self.count = len(self.counter_id)

        # self.inside_id = current_inside_id
        

    def _inside_zone(self, center_x: int, center_y: int) -> bool:
        return self.mask[center_y, center_x] == 255
    
    def draw(self, frame):
        overlay = frame.copy()
        cv2.fillPoly(overlay, [self.points], (0, 0, 255))
        alpha = 0.5
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        for cx, cy in self.centers:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        cv2.polylines(frame, [self.points], isClosed=True, color=(0, 0, 255), thickness=2)

        cv2.putText(frame, f'Count: {self.count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame
    

class MultipleLaneZoneCounter(LaneZoneCounter):
    def __init__(self, list_points: list[list[tuple]], frame_size: tuple, colors: list[tuple], max_speed: list[float]):
        # Gọi lớp cha để khởi tạo thông số nền tảng
        super().__init__(points=list_points[0], frame_size=frame_size) 
        
        self.list_points = [np.array(pts, dtype=np.int32) for pts in list_points]
        
        # --- BƯỚC CONVERT MÀU SẮC AN TOÀN ---
        # Ép kiểu dữ liệu màu từ chuỗi "(B, G, R)" trong YAML thành Tuple số nguyên (B, G, R)
        cleaned_colors = []
        for color in colors:
            if isinstance(color, str):
                color = color.replace('(', '').replace(')', '')
                b, g, r = map(int, color.split(','))
                cleaned_colors.append((b, g, r))
            else:
                cleaned_colors.append(tuple(map(int, color)))

        # map vòng nếu số lượng màu ít hơn số lượng vùng
        if len(cleaned_colors) < len(list_points):
            cleaned_colors = (cleaned_colors * (len(list_points) // len(cleaned_colors) + 1))[:len(list_points)]
        self.colors = cleaned_colors
        # ------------------------------------
        # --- BƯỚC XỬ LÝ TỐC ĐỘ TỐI ĐA AN TOÀN ---
        if max_speed is None:
            max_speed = [0.0] * len(list_points)
        else:
            self.max_speed = max_speed
            if len(self.max_speed) != len(list_points):
                raise ValueError("Length of max_speed must match length of list_points")
            
        self.track_ids = {}  # theo dõi vượt quá tốc độ cho từng track_id
        # ------------------------------------

        # Khởi tạo bộ đếm độc lập cho từng vùng
        self.count = [0] * len(list_points)
        self.inside_id = [set() for _ in range(len(list_points))]
        
        # Tạo danh sách mặt nạ (masks) cho từng vùng
        self.list_masks = []
        for pts in self.list_points:
            mask = np.zeros((frame_size[1], frame_size[0]), dtype=np.uint8)
            cv2.fillPoly(mask, [pts], 255)
            self.list_masks.append(mask)

    def update_count(self, detections: list[dict]):
        self.centers = []
        current_inside_id = [set() for _ in range(len(self.list_masks))]
        current_speeds = set() # lưu id vi phạm tốc độ tối đa trong frame hiện tại
        active_set = set() # lưu id đang hoạt động trong frame hiện tại

        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            track_id = detection['track_id']
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            active_set.add(track_id) # lưu id đang hoạt động trong frame hiện tại
            
            speed = detection.get('speed', 0.0)


            if center_x < 0 or center_x >= self.frame_size[0] or center_y < 0 or center_y >= self.frame_size[1]:
                continue

            # Kiểm tra xem tâm vật thể nằm trong vùng nào
            for i, mask in enumerate(self.list_masks):
                if mask[center_y, center_x] == 255:
                    current_inside_id[i].add(track_id)
                    # --- BƯỚC KIỂM TRA TỐC ĐỘ TỐI ĐA ---
                    if speed > self.max_speed[i]:
                        current_speeds.add(track_id)
                        detection['speed_violation'] = True  # Đánh dấu vi phạm tốc độ trong detection : để đổi màu theo dõi

            self.centers.append((center_x, center_y, detection.get('speed_violation', False)))  # Thêm thông tin vi phạm tốc độ vào tâm điểm
    
        self.count = [len(ids) for ids in current_inside_id]
        self.inside_id = current_inside_id
        self.track_ids = current_speeds

    def draw(self, frame):
        overlay = frame.copy()

        # 1. Vẽ các tâm điểm vật thể hiện tại (màu trắng)
        for cx, cy, speed_violation in self.centers:
            color = (0, 0, 255) if speed_violation else (255, 255, 255)
            cv2.circle(frame, (cx, cy), 5, color, -1)

        # 2. Vẽ phủ màu tất cả các vùng lên overlay và vẽ viền lên frame
        for pts, color in zip(self.list_points, self.colors):
            cv2.fillPoly(overlay, [pts], color)
            cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=2)

        # 3. Trộn overlay mờ vào frame gốc (Thực hiện NGOÀI vòng lặp)
        alpha = 0.4
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # 4. In chữ số đếm của từng vùng lên góc màn hình (Xếp hàng dọc, không đè nhau)
        for i, color in enumerate(self.colors):
            text_y = 10 + i * 20
            cv2.putText(frame, f'Zone {i+1}: {self.count[i]}', (10, text_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        return frame
    
import cv2
import numpy as np


class LineCounter:
    def __init__(self, points: list[tuple]):
        self.points = points
        self.count = 0
        self.counter_id = set() # tránh trùng ID đã đếm
        self.pre_side_by_id = {} # lưu trạng thái trước đó của từng ID

    def update_count(self, detections: list[dict]):
        self.centers = []
        active_ids = set()

        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            track_id = detection['track_id']
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            active_ids.add(track_id) # lưu ID đang hoạt động

            self.centers.append((center_x, center_y))
            
            # Lưu trạng thái hiện tại cho ID
            pre_side = self.pre_side_by_id.get(track_id, None)
            cur_side = center_y - self.points[0][1]

            # Kiểm tra xem có crossing không
            crossed = False
            if pre_side is not None:
                if (pre_side < 0 and cur_side >= 0) or (pre_side >= 0 and cur_side < 0):
                    crossed = True
            
            # Cập nhật trạng thái hiện tại cho ID
            if crossed and track_id not in self.counter_id:
                self.count += 1
                self.counter_id.add(track_id)

            self.pre_side_by_id[track_id] = cur_side # cập nhật trạng thái cho ID

        # Tối ưu mem và các thuật toán bytetrack và deepsort không tự xóa ID khi không còn hoạt động và tái sử dụng, nên ta sẽ xóa trạng thái của những ID không còn hoạt động
        # Nếu không xóa khi được tái sư dụng sẽ gọi đến giá trị cũ của ID đó
        stable_ids = set(self.pre_side_by_id.keys() - active_ids) # ID không còn hoạt động
        for stable_id in stable_ids:
            del self.pre_side_by_id[stable_id] # xóa trạng thái của ID không còn hoạt động


            # if self._crossed_line(center_x, center_y) and track_id not in self.counter_id:
            #     self.count += 1
            #     self.counter_id.add(track_id)
        

    def _crossed_line(self, center_x: int, center_y: int) -> bool:
        return abs(center_y - self.points[0][1]) < 5 and self.points[0][0] <= center_x <= self.points[1][0]
    
    def draw(self, frame):

        for cx, cy in self.centers:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        cv2.line(frame, self.points[0], self.points[1], (0, 0, 255), 2)

        cv2.putText(frame, f'Count: {self.count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame
    

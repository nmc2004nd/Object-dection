import cv2
import numpy as np


class LineCounter:
    def __init__(self, line_position: list[tuple]):
        self.line_position = line_position
        self.count = 0
        self.counter_id = set() # tránh trùng ID đã đếm

    def update_count(self, detections: list[dict]):
        self.centers = []

        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            track_id = detection['track_id']
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            self.centers.append((center_x, center_y))

            if self._crossed_line(center_x, center_y) and track_id not in self.counter_id:
                self.count += 1
                self.counter_id.add(track_id)
        

    def _crossed_line(self, center_x: int, center_y: int) -> bool:
        return abs(center_y - self.line_position[0][1]) < 5 and self.line_position[0][0] <= center_x <= self.line_position[1][0]
    
    def draw(self, frame):

        for cx, cy in self.centers:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        cv2.line(frame, self.line_position[0], self.line_position[1], (0, 0, 255), 2)

        cv2.putText(frame, f'Count: {self.count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame
    
class ZoneCounter:
    def __init__(self, zone_position: list[tuple]):
        self.zone_position = zone_position
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
        x1, y1 = self.zone_position[0]
        x2, y2 = self.zone_position[1]
        return x1 <= center_x <= x2 and y1 <= center_y <= y2
    
    def draw(self, frame):
        for cx, cy in self.centers:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        cv2.rectangle(frame, self.zone_position[0], self.zone_position[1], (0, 0, 255), 2)

        cv2.putText(frame, f'Count: {self.count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame
    
class LaneZoneCounter:
    def __init__(self, points: list[tuple], frame_size: tuple):
        self.frame_size = frame_size
        self.points = np.array(points, dtype=np.int32)
        self.count = 0
        self.inside_id = set() # tránh trùng

        # Tạo mặt nạ cho khu vực được xác định bởi các điểm
        self.mask = np.zeros((frame_size[1], frame_size[0]), dtype=np.uint8)
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

            if center_x < 0 or center_x >= self.frame_size[0] or center_y < 0 or center_y >= self.frame_size[1]:
                continue

            if self._inside_zone(center_x, center_y):
                current_inside_id.add(track_id)


        self.count = len(current_inside_id)

        self.inside_id = current_inside_id

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
    
import cv2
import numpy as np


class LineCounter:
    def __init__(self, points: list[tuple]):
        self.points = points
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
        return abs(center_y - self.points[0][1]) < 5 and self.points[0][0] <= center_x <= self.points[1][0]
    
    def draw(self, frame):

        for cx, cy in self.centers:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        cv2.line(frame, self.points[0], self.points[1], (0, 0, 255), 2)

        cv2.putText(frame, f'Count: {self.count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame
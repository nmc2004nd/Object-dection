import cv2
import numpy as np
from pathlib import Path
import logging

class SpeedEstimator:
    def __init__(self, pixel_per_meter: float, fps: int, buffer_size: int = 5):
        self.pixel_per_meter = pixel_per_meter
        self.fps = fps
        self.buffer_size = buffer_size

        self.track_buffers = {}  # lưu trữ các buffer cho từng track_id
        self.current_speeds = {}  # lưu trữ tốc độ hiện tại cho từng track_id
        self.frame_count = 0  # đếm số frame đã xử lý

    def update(self, detections: list[dict], current_frame: int):
        # self.frame_count += 1
        active_tracks = set()

        for detection in detections:
            track_id = detection['track_id']
            active_tracks.add(track_id)
            
            x1, y1, x2, y2 = detection['bbox']
            # Tối ưu hóa phép chia lấy nguyên
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            if track_id not in self.track_buffers:
                self.track_buffers[track_id] = []

            # Thêm vị trí hiện tại vào buffer
            self.track_buffers[track_id].append((center_x, center_y, current_frame))

            max_buffer_size = max(self.buffer_size * 2, 10)

            # Giữ buffer không vượt quá kích thước tối đa
            if len(self.track_buffers[track_id]) > max_buffer_size:
                self.track_buffers[track_id].pop(0)

            if len(self.track_buffers[track_id]) >= self.buffer_size:
                speed = self._calculate_speed(self.track_buffers[track_id][-self.buffer_size:])
                self.current_speeds[track_id] = speed
                detection['speed'] = speed  
                
        # TÙY CHỌN: Dọn dẹp bộ nhớ cho các track không còn xuất hiện (Tránh rò rỉ bộ nhớ)
        # nếu hệ thống chạy tracking thời gian thực trong thời gian dài
        # self._clean_stale_tracks(active_tracks)

    def _calculate_speed(self, buffer: list[tuple]) -> float:
        if not buffer or len(buffer) < 2:
            return 0.0

        total_distance_px = 0.0

        for i in range(1, len(buffer)):
            x1, y1, _ = buffer[i - 1]
            x2, y2, _ = buffer[i]
            distance_px = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_distance_px += distance_px

        time_elapsed = (buffer[-1][2] - buffer[0][2]) / self.fps

        if time_elapsed > 0:
            speed_m_per_s = (total_distance_px / self.pixel_per_meter) / time_elapsed
            speed_km_per_h = speed_m_per_s * 3.6
            return round(speed_km_per_h, 2)
            
        return 0.0 # Tránh trả về None nếu time_elapsed == 0
        
    def _clean_stale_tracks(self, active_tracks: set):
        """Xóa các track không còn xuất hiện để giải phóng RAM"""
        stale_tracks = [tid for tid in self.track_buffers if tid not in active_tracks]
        for tid in stale_tracks:
            del self.track_buffers[tid]
            if tid in self.current_speeds:
                del self.current_speeds[tid]
        
    def get_current_speeds(self):
        return self.current_speeds
    
    def reset(self):
        self.track_buffers.clear()
        self.current_speeds.clear()
        self.frame_count = 0
        logging.info("SpeedEstimator has been reset.")
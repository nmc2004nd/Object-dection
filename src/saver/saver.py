import os
import cv2

class ResultsSaver:
    def __init__(
        self, 
        save_dir: str = "outputs",
        save_frame: bool = True,
        save_detections: bool = False,
        save_crop: bool = False,
                 
    ):
        self.save_dir = save_dir
        self.save_frame_flag = save_frame
        self.save_detections_flag = save_detections
        self.save_crop_flag = save_crop

        os.makedirs(save_dir, exist_ok=True)

    def save(self, frame, detections, frame_id):
        if self.save_frame_flag:
            self._save_frame(frame, detections, frame_id)

        if self.save_detections_flag:
            self._save_detections(detections, frame_id)

        if self.save_crop_flag:
            self._save_crop(frame, detections, frame_id)

    def _save_frame(self, frame, detections, frame_id):
        save_path = os.path.join(self.save_dir, f"frame_{frame_id:04d}.jpg")
        cv2.imwrite(save_path, frame)

    def _save_detections(self, detections, frame_id):
        save_path = os.path.join(self.save_dir, f"frame_{frame_id:04d}.txt")
        with open(save_path, 'w', encoding='utf-8') as f:
            for det in detections:
                x1, y1, x2, y2 = det['bbox']
                conf = det['conf']
                cls = det['cls']
                f.write(f"{cls} {conf:.4f} {x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f}\n")
    
    def _save_crop(self, frame, detections, frame_id):
        for idx, det in enumerate(detections):
            x1, y1, x2, y2 = map(int, det['bbox'])
            crop = frame[y1:y2, x1:x2]
            save_path = os.path.join(self.save_dir, f"frame_{frame_id:04d}_crop_{idx:02d}.jpg")
            cv2.imwrite(save_path, crop)
            
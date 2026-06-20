from ultralytics import YOLO

class YOLODetector: # detect 1 frame nên không cần stride
    def __init__(
        self, 
        model_path: str,
        conf : float = 0.25,
        iou: float = 0.45,
        classes: list[int] = None,
        max_det: int = 100,
        device: int | str = 0,
    ):
        self.model = YOLO(model_path)
        self.conf = conf
        self.iou = iou
        self.classes = classes
        self.max_det = max_det
        self.device = device

    def detect(self, frame):
    #     results = self.model.predict(
    #         source=frame,
    #         conf=self.conf,
    #         iou=self.iou,
    #         classes=self.classes,
    #         max_det=self.max_det,
    #         device=self.device,
    #         verbose=False # tắt log của YOLO
    #     )[0] #do predict trả về một list các kết quả
    # # có thể dùng dir để xem các property của results
    #     detections = []
    #     for box in results.boxes:
    #         x1, y1, x2, y2 = box.xyxy[0].tolist() # lấy tọa độ bounding box
    #         conf = float(box.conf[0].item()) # lấy confidence score
    #         cls = int(box.cls[0].item()) # lấy class id

    #         detections.append({
    #             'bbox': [x1, y1, x2, y2],
    #             'conf': conf,
    #             'cls': cls
    #         })

        results = self.model.track(
            source=frame,
            conf=self.conf,
            iou=self.iou,
            classes=self.classes,
            max_det=self.max_det,
            device=self.device,
            persist=True, # duy trì ID của đối tượng qua các frame
            tracker = "bytetrack.yaml", # sử dụng thuật toán ByteTrack để theo dõi đối tượng
            # tracker = "botsort.yaml", # sử dụng thuật toán BoTSORT để theo dõi đối tượng, với conf cao hơn để giảm false positive
            verbose=False, # tắt log của YOLO
        )[0] #do track trả về một list các kết quả
    # có thể dùng dir để xem các property của results

        detections = []

        for box, id in zip(results.boxes, results.boxes.id):
            x1, y1, x2, y2 = box.xyxy[0].tolist() # lấy tọa độ bounding box
            conf = float(box.conf[0].item()) # lấy confidence score
            cls = int(box.cls[0].item()) # lấy class id
            id = int(id) # lấy ID của đối tượng

            detections.append({
                'bbox': [x1, y1, x2, y2],
                'conf': conf,
                'cls': cls,
                'track_id': id
            })

        return detections

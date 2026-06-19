import cv2
from scripts import saver
from visualize import draw_boxes
from detector import YOLODetector
from saver import ResultsSaver

INPUT_PATH = "D:/NMC/Object-detection/inputs/videos/videoplayback.mp4"
VID_STRIDE = 1 # 1: downsample video, 0: use original video
MODEL_PATH = "D:/NMC/Object-detection/models/yolo26n.pt"
OUTPUT_PATH = "D:/NMC/Object-detection/outputs/videos/output.mp4"
SAVE_DIR = "D:/NMC/Object-detection/outputs"

# saver = ResultsSaver(
#     save_dir=SAVE_DIR,
#     # save_frame=True,
#     # save_txt=True,
#     # save_crop=True
# )

def main():
    detector = YOLODetector(
        MODEL_PATH, 
        # conf=0.25, 
        # iou=0.45, 
        classes=[2], 
        # max_det=100, 
        device=0)
    
    cap = cv2.VideoCapture(INPUT_PATH)

    frame_id = 0

    detections = []

    if not cap.isOpened():
        print("Khong the mo video stream or file")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % VID_STRIDE == 0:
            detections = detector.detect(frame)
            # saver.save(frame, detections, frame_id)
        frame_id += 1

        frame = draw_boxes(frame, detections, class_names=detector.model.names)
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
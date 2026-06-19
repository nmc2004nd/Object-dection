import cv2

def draw_boxes(frame, detections, class_names=None, color=(0, 255, 0), thickness=2):
    """
    Vẽ bounding boxes và putText lên ảnh.

    Args:
        frame (numpy.ndarray): The input frame.
        detections (list): danh sách các detections, mỗi detection là một dict chứa 'bbox', 'conf', và 'cls'.
        class_names (list): danh sách tên lớp.
        color (tuple): màu sắc vẽ bounding box (BGR format).
        thickness (int): độ dày của bounding box và text.

    Returns:
        numpy.ndarray: The frame with drawn bounding boxes.
    """
    for detection in detections:
        x1, y1, x2, y2 = map(int, detection['bbox']) # hàm rectangle yêu cầu tọa độ nguyên
        conf = detection['conf']
        cls_id = detection['cls']

        label = class_names[cls_id] if class_names else str(cls_id) # nếu có class names thì dùng, không thì dùng id
        text = f"{label}: {conf:.2f}"

        # Vẽ bounding box và text lên frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, thickness)
        # vẽ background cho text để dễ đọc hơn
        cv2.rectangle(frame, (x1, y1 - text_height - 4), (x1 + text_width, y1), color, -1)
        cv2.putText(frame, text, (x1 + 2, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 255], 2)
    return frame
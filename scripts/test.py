import cv2
import numpy as np

video_path = r"D:/NMC/Object-detection/inputs/videos/videoplayback.mp4"

cap = cv2.VideoCapture(video_path)

ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Không thể đọc video")

points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print((x, y))

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Frame", mouse_callback)

while True:
    display = frame.copy()

    for p in points:
        cv2.circle(display, p, 5, (0, 0, 255), -1)

    if len(points) >= 2:
        cv2.polylines(
            display,
            [np.array(points, dtype=np.int32)],
            False,
            (0, 255, 0),
            2
        )

    cv2.imshow("Frame", display)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break

    elif key == ord("c"):
        points.clear()

cv2.destroyAllWindows()

print("Points =", points)
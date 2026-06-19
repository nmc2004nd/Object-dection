from ultralytics import YOLO 
import cv2

# Load a model

model = YOLO('yolo26n.pt') 

# path

video_path = 'D:/NMC/Object-detection/inputs/videos/videoplayback.mp4'
output_path = 'D:/NMC/Object-detection/outputs/videos/output_video.mp4'

# Mở video
cap =  cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

# thiết lập VideoWriter để lưu video đầu ra
fourcc = cv2.VideoWriter_fourcc(*'avc1')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# # Run inference on an image
results = model.predict(source='D:/NMC/Object-detection/inputs/images/anh_1.jpg', 
              save=True, 
              device = 0,
              conf=0.25,
              classes = [2],
              max_det = 3)

print(dir(results[0].boxes))

# Run inference on a video

# results = model.predict(source=video_path,
#                         stream=True, # tạo ra một generator để xử lý từng frame một cách hiệu quả
#                         device = 0,
#                         conf=0.25,
#                         classes = [2],
#                         vid_stride = 3, # bước nhảy để xử lý mỗi frame 
#                         )


# print(dir(results))
# for result in results:
#     annotated_frame = result.plot()  # Get the annotated frame
#     out.write(annotated_frame)  # Write the annotated frame to the output video

# # Release resources
# cap.release()
# out.release()
# cv2.destroyAllWindows()

# print(f"Output video saved to: {output_path}")
from pathlib import Path

from core.settings_loader import load_settings
from core.logging_setup import setup_logging

from src.pipeline import DetectionPipeline

def main():
    # Load settings
    config = load_settings()
    
    # Setup logging
    setup_logging()

    # Tạo các thư mục cần thiết
    for folder in ['inputs', 'outputs', 'logs', 'models']:
        Path(folder).mkdir(parents=True, exist_ok=True)

    INPUT_PATH = 'inputs/videos/videoplayback.mp4'
    VID_STRIDE = 1
    DISPLAY = True
    COUNTER_TYPE = config['counter'][0]['type']  # 'line', 'zone', 'lane_zone', or 'multiple_lane_zone'

    # Kiểm tra xem có cấu hình counter trong file YAML không
    if 'counter' in config and len(config['counter']) > 0:
        counter_cfg = config['counter'][0]
        COUNTER_TYPE = counter_cfg.get('type', 'lane_zone')
    else:
        raise ValueError("Cấu hình 'counter' không tồn tại hoặc trống trong file settings!")
    


    # Initialize the detection pipeline
    pipeline = DetectionPipeline(config)
    input_path = Path(INPUT_PATH)
    # Lấy trực tiếp thông tin cấu hình từ YAML
    counter_kwargs = {
        'points': counter_cfg.get('points'),
        'colors': counter_cfg.get('colors', [(0, 0, 255)])  # Mặc định là màu Đỏ (BGR)
    }

    # Run the detection pipeline on the video
    if input_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        pipeline.run_video(
            video_path=input_path, 
            counter_type=COUNTER_TYPE, 
            counter_kwargs=counter_kwargs, 
            vid_stride=VID_STRIDE, 
            display=DISPLAY)
        
    else:
        print(f"Unsupported input file format: {input_path.suffix}")
        print("Please provide a video file with one of the following extensions: .mp4, .avi, .mov, .mkv")

if __name__ == "__main__":
    main()
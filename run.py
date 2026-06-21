from pathlib import Path

from core.settings_loader import load_settings
from core.logging_setup import setup_logging

from src.pipeline import DetectionPipeline

def main():
    # Load settings
    config = load_settings()
    
    # Setup logging
    setup_logging()

    Path('inputs').mkdir(parents=True, exist_ok=True)
    Path('outputs').mkdir(parents=True, exist_ok=True)
    Path('logs').mkdir(parents=True, exist_ok=True)
    Path('models').mkdir(parents=True, exist_ok=True)

    INPUT_PATH = 'inputs/videos/videoplayback.mp4'
    COUNTER_TYPE = 'line'  # Options: 'line', 'zone', 'lane_zone'
    VID_STRIDE = 1
    DISPLAY = True

    # Initialize the detection pipeline
    pipeline = DetectionPipeline(config)
    input_path = Path(INPUT_PATH)
    counter_kwargs = {}

    if COUNTER_TYPE == 'line':
        counter_kwargs['points'] = [(100, 200), (500, 200)]  
    elif COUNTER_TYPE == 'zone':
        counter_kwargs['points'] = [(200, 50), (500, 200)]  
    elif COUNTER_TYPE == 'lane_zone':
        counter_kwargs['points'] = [(203, 83), (382, 83), (482, 200), (133, 200)] 


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
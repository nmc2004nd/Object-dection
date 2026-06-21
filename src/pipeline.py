import cv2
from pathlib import Path
import logging

from src.detector.detector import YOLODetector
from src.saver.saver import ResultsSaver
from src.visualize.visualize import draw_boxes
from src.counter.line_counter import LineCounter
from src.counter.zone_counter import ZoneCounter, LaneZoneCounter

logger = logging.getLogger('src')

class DetectionPipeline:
    def __init__(self, config):
        self.config = config

        # Initialize the YOLO detector
        model_path = Path(config['data']['model']) / f"{config['detector']['type']}.pt"
        self.detector = YOLODetector(
            model_path= str(model_path),
            conf=config['detector']['conf_threshold'],
            iou=config['detector']['iou_threshold'],
            classes=(config['detector'].get('classes', None)),        
            max_det=config['detector']['max_det'],
            device=config['detector']['device'],
        )

        # Initialize the results saver
        self.saver = ResultsSaver(
            save_dir=config['data']['output'],
            save_frame=config['saver'].get('save_images', True),
            save_detections=config['saver'].get('save_detections', False),
            save_crop=config['saver'].get('save_crops', False),
        )

        # Initialize the line and zone counters
        self.counter = None

        logger.info("Detection pipeline initialized.")

    def initialize_counter(self, counter_type, **kwargs):
        if counter_type == 'line':
            points = kwargs.get('points', None)
            self.counter = LineCounter(points=points)
            logger.info("Line counter initialized.")
        elif counter_type == 'zone':
            points = kwargs.get('points', None)
            self.counter = ZoneCounter(points=points)
            logger.info("Zone counter initialized.")
        elif counter_type == 'lane_zone':
            points = kwargs.get('points', None)
            frame_size = kwargs.get('frame_size', None)
            self.counter = LaneZoneCounter(points=points, frame_size=frame_size)
            logger.info("Lane zone counter initialized.")
        else:
            raise ValueError(f"Unsupported counter type: {counter_type}")
        
    def run_video(
            self, 
            video_path, 
            counter_type = 'lane_zone', 
            counter_kwargs = None, 
            vid_stride = 1, 
            display = True
        ):

        cap = cv2.VideoCapture(str(video_path))

        ret, frame = cap.read()

        if not ret:
            logger.error(f"Failed to read video: {video_path}")
            return
        
        # Initialize the counter based on the provided type and kwargs
        if counter_kwargs is None:
            counter_kwargs = {}
        
        counter_kwargs['frame_size'] = frame.shape[:2]  # Pass frame size to the counter if needed
        self.initialize_counter(counter_type, **counter_kwargs)

        frame_id = 0

        detections = []

        while True:
            frame_id += 1

            if frame_id == 1 or frame_id % vid_stride == 0:
                detections = self.detector.detect(frame)

                if self.config['saver'].get('save_images', False):
                    self.saver.save(frame, detections, frame_id)

            if self.counter:
                self.counter.update_count(detections)

            frame = draw_boxes(frame, detections)

            if self.counter:
                frame = self.counter.draw(frame)
            if display:
                cv2.imshow("Detection Pipeline", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.info("Video processing interrupted by user.")
                    break

            ret, frame = cap.read()
            if not ret:
                logger.info("End of video reached.")
                break

        cap.release()
        if display:
            cv2.destroyAllWindows()

        logger.info('Video processing completed.')
        if self.counter:
            logger.info(f"Final counts: {self.counter.count}")


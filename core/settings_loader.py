import yaml
import logging.config
import os
from pathlib import Path
from dotenv import load_dotenv

def load_settings():
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    
    config_path = Path('config/settings.yaml')
    if not config_path.exists():
        raise FileNotFoundError(f"Settings file not found at {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        settings = yaml.safe_load(f)

    ## Override settings with environment variables if they exist
    # os.getenv : default return  str
    # App settings
    if os.getenv('APP_ENV'):
        settings['app']['env'] = os.getenv('APP_ENV')
    if os.getenv('APP_NAME'):
        settings['app']['name'] = os.getenv('APP_NAME')

    # Data settings
    if os.getenv('INPUT_PATH'):
        settings['data']['input'] = os.getenv('INPUT_PATH')
    if os.getenv('OUTPUT_PATH'):
        settings['data']['output'] = os.getenv('OUTPUT_PATH')
    if os.getenv('MODEL_PATH'):
        settings['data']['model'] = os.getenv('MODEL_PATH')

    # Detector settings
    if os.getenv('DETECTOR_TYPE'):
        settings['detector']['type'] = os.getenv('DETECTOR_TYPE')
    if os.getenv('DETECTOR_CONF_THRESHOLD'):
        settings['detector']['conf_threshold'] = float(os.getenv('DETECTOR_CONF_THRESHOLD'))
    if os.getenv('DETECTOR_IOU_THRESHOLD'):
        settings['detector']['iou_threshold'] = float(os.getenv('DETECTOR_IOU_THRESHOLD'))
    if os.getenv('DETECTOR_MAX_DET'):
        settings['detector']['max_det'] = int(os.getenv('DETECTOR_MAX_DET'))
    if os.getenv('DETECTOR_DEVICE'):
        settings['detector']['device'] = os.getenv('DETECTOR_DEVICE')
    if os.getenv('DETECTOR_CLASSES'): # 1,2,3 -> ['1','2','3'] -> [1,2,3]
        settings['detector']['classes'] = [int(x) for x in os.getenv('DETECTOR_CLASSES').split(',')] if os.getenv('DETECTOR_CLASSES').lower() != 'none' else None

    # Saver settings
    if os.getenv('SAVER_SAVE_IMAGES'):
        settings['saver']['save_images'] = os.getenv('SAVER_SAVE_IMAGES').lower() == 'true'
    if os.getenv('SAVER_SAVE_VIDEOS'):
        settings['saver']['save_videos'] = os.getenv('SAVER_SAVE_VIDEOS').lower() == 'true'
    if os.getenv('SAVER_SAVE_DETECTIONS'):
        settings['saver']['save_detections'] = os.getenv('SAVER_SAVE_DETECTIONS').lower() == 'true'
    if os.getenv('SAVER_SAVE_CROPS'):
        settings['saver']['save_crops'] = os.getenv('SAVER_SAVE_CROPS').lower() == 'true'

    # Tracker settings
    if os.getenv('TRACKER_TYPE'):
        settings['tracker']['type'] = os.getenv('TRACKER_TYPE')

    return settings
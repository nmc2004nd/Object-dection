import yaml
import logging.config
from pathlib import Path


def setup_logging():
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    with open('config/logging.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)
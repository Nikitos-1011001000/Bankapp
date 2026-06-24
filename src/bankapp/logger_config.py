import logging
import sys
from pathlib import Path


def setup_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    project_root = Path(r"C:\Users\nkt91\OneDrive\Desktop\P")
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f'{name}.log'

    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

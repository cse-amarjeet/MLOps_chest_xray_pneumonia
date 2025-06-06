import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Constants
LOG_DIR_NAME = "logs"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

def get_project_root() -> str:
    """Returns the absolute path to the project root."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  

def get_log_directory() -> str:
    """Returns the absolute path to the log directory in project root."""
    log_dir = os.path.join(get_project_root(), LOG_DIR_NAME)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def get_log_file_path(log_dir: str) -> str:
    """Generates a timestamped log filename in the specified directory."""
    filename = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".log"
    return os.path.join(log_dir, filename)

def configure_logger() -> None:
    """
    Configures the root logger with rotating file and console handlers.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    log_dir = get_log_directory()
    log_file_path = get_log_file_path(log_dir)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Avoid adding handlers multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

# Initialize the logger
configure_logger()

import logging
import os

# Create logs folder
os.makedirs("logs", exist_ok=True)

# Create our own logger
logger = logging.getLogger("HR_COPILOT")
logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.propagate = False

# Create file handler
file_handler = logging.FileHandler(
    "logs/hr_copilot.log"
)

file_handler.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)

# Add handler only once
if not logger.handlers:
    logger.addHandler(file_handler)
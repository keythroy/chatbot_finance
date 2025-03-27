import logging
import os
from datetime import datetime

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s - %(asctime)s ',
    handlers=[
        logging.FileHandler(os.path.join('app','logs', 'app.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_error(message):
    logger.error(message)

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_debug(message):
    logger.debug(message)

def log_critical(message):
    logger.critical(message)
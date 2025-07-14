import logging
import os

LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def setup_logger():
    """
    Configura o logger para o formato desejado.
    """
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger(__name__)
    
    return logger

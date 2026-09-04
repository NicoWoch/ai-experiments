import logging
import os.path


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(os.path.dirname(__file__), 'data/app.log'), mode='w', encoding='utf-8'),
        ],
    )
    
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info('Application started')

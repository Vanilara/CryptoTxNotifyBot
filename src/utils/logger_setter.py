import logging

from core.config import settings



logging.basicConfig(
    filename=f'{settings.paths.LOGS_PATH}/logs.log',
    filemode='a',
    level=logging.DEBUG,                  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'        
)

logging.getLogger('asyncio').setLevel(logging.ERROR)
starter_logger = logging.getLogger('Initial')

class Loggable:
    def __init__(self, logger_name: str | None = None):
        self.logger = logging.getLogger(logger_name or self.__class__.__name__)
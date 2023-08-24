import logging
import logging.config

logging.config.fileConfig("logs/logging.conf")
logger = logging.getLogger("sLogger")
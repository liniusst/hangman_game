import logging
import logging.config

logging.config.fileConfig("frontend/logs/logging.conf")
logger = logging.getLogger("sLogger")

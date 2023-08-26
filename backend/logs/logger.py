import logging
import logging.config

logging.config.fileConfig("backend/logs/logging.conf")
logger = logging.getLogger("sLogger")

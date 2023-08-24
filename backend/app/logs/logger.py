import logging
import logging.config

logging.config.fileConfig("app/logs/logging.conf")
logger = logging.getLogger("sLogger")
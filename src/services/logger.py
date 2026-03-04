import os
import logging
from dotenv import load_dotenv

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

if LOG_LEVEL.lower() not in ["debug", "info", "warning", "error", "critical"]:
    logger.warning("LOG_LEVEL is not correct. Defaulting to INFO")
    LOG_LEVEL = "INFO"
else:
    logger.info("Setting log level to %s", LOG_LEVEL.upper())

logger.setLevel(LOG_LEVEL.upper())

debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical

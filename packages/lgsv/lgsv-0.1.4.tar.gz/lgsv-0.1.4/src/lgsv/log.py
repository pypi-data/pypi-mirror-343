"""
logging.
"""

import logging
from lgsv import setting

logging.basicConfig(format="%(levelname)-8s %(name)s: %(message)s")
logger = logging.getLogger("lgsv")
logger.setLevel(setting.global_config["loglevel"])

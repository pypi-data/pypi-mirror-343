# 移除或注释掉原来的导入
#: code: utf-8

from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__version__ = "1.0.0"

__all__ = ["AgentIdClient", "VERSION", "AgentId" "logger"]


import logging
from agentid.env import Environ


def get_logger(name=__name__, level=Environ.LOG_LEVEL.get(logging.INFO)) -> logging.log:
    """
    Set up the log for the agentid module.
    """
    log = logging.getLogger(name)
    log.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    return log


logger = get_logger(name="agentid", level=Environ.LOG_LEVEL.get(logging.INFO))


def initialize(_log: logging.log) -> None:
    global logger
    """
    Initialize the agentid module.
    """
    logger.info("Initializing agentid module.")
    # Perform any necessary initialization here
    # For example, you might want to set up logging or configuration
    # log.info("AgentId initialized successfully.")
    logger = _log

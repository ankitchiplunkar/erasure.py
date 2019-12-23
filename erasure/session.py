import sys
import logging
from web3 import Web3
from erasure.settings import (
    LOG_STDOUT,
    LOG_FORMAT,
    LOG_LEVEL,
)


logger = logging.getLogger(__name__)


def setup_logging():
    """
    Add logging format to logger used for debugging and info
    """
    handler = logging.StreamHandler(
        sys.stdout if LOG_STDOUT else sys.stderr)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(LOG_LEVEL)

    # removing logs from noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("web3").setLevel(logging.WARNING)


def init_web3(node_url):
    return Web3(Web3.HTTPProvider(node_url))


def initialize_erasure_account(w3, private_key):
    return w3.eth.account.from_key(private_key)

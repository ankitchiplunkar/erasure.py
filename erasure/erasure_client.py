import logging
from erasure.contracts import (
    MAINNET_CONTRACTS,
    RINKEBY_CONTRACTS,
)

logger = logging.getLogger(__name__)


class ErasureClient():
    """
    Main entrypoint for the erasuer python client
    """

    def __init__(self, w3, mode, version):
        self.w3 = w3
        if mode == 'test':
            logger.info(f"Running erasure client in {mode} mode with {version} contracts")
            self.contract_address = RINKEBY_CONTRACTS[version]
        elif mode == 'prod':
            logger.info(f"Running erasure client in {mode} mode with {version} contracts")
            self.contract_address = MAINNET_CONTRACTS[version]
        else:
            raise KeyError(f"Mode {mode} is not supported")

    
    def create_feed(self):
        return True
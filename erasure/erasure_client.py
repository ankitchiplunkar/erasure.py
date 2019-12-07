import logging
from erasure.contracts import (
    MAINNET_CONTRACTS,
    RINKEBY_CONTRACTS,
)
from erasure.session import initialize_erasure_account
from erasure.settings import ERASURE_ACCOUNT_PRIVATE_KEY
from erasure.utils import (
    initialize_contract,
    get_gas_price,
)


logger = logging.getLogger(__name__)


class ErasureClient():
    """
    Main entrypoint for the erasuer python client
    """

    def __init__(self, w3, mode, version):
        self.w3 = w3
        self.account = initialize_erasure_account(
            w3, ERASURE_ACCOUNT_PRIVATE_KEY)
        # Initializing contract addresses
        if mode == 'rinkeby':
            logger.info(f"Connecting to Rinkeby testnet")
            assert w3.eth.chainId == 4
            logger.info(f"Running erasure client with {version} contracts")
            self.contract_dict = RINKEBY_CONTRACTS[version]
        elif mode == 'mainnet':
            logger.info(f"Connecting to ethereum mainnet")
            assert w3.eth.chainId == 1
            logger.info(f"Running erasure client with {version} contracts")
            self.contract_dict = MAINNET_CONTRACTS[version]
        else:
            raise KeyError(f"Mode {mode} is not supported")
        # Initializing contracts
        self.feed_factory = initialize_contract(
            w3=self.w3,
            contract_dict=self.contract_dict,
            contract_name="FeedFactory")

    def create_feed(self, metadata=""):
        # getting the gas price
        gas_price = self.w3.toWei(get_gas_price(), 'gwei')
        create_feed_txn = self.feed_factory.functions.createExplicit(
            self.account.address,  # address of the owner of the feed
            # address of the erasure posts contract
            self.contract_dict['ErasurePosts'],
            bytes(metadata, 'utf-8')).buildTransaction({
                'chainId': self.w3.eth.chainId,
                'gasPrice': gas_price,
                'gas': 3*10**5,
                'nonce': self.w3.eth.getTransactionCount(self.account.address),
            })
        signed_txn = self.w3.eth.account.sign_transaction(
            create_feed_txn, self.account.key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        logger.info(f"Sent the transaction {tx_hash.hex()} to create feed")
        pass

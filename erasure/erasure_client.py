import logging
from math import ceil
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
        self.version = version
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
            contract_address=self.contract_dict["FeedFactory"],
            contract_name="FeedFactory")
        self.feed_template = initialize_contract(
            w3=self.w3,
            contract_address=None,
            contract_name="Feed")

    def create_feed(self, proofhash='0x', metadata='0x'):
        logger.info(f"Creating erasure with protocol version {self.version}")
        logger.info(
            f"Creating erasure feed for the user {self.account.address}")
        logger.info(
            f"Creating erasure feed at the operator {self.contract_dict['ErasurePosts']}")
        # getting the gas price
        gas_price = self.w3.toWei(get_gas_price(), 'gwei')
        # get call data to create feed
        initialize_feed_call_data = self.feed_template.encodeABI('initialize', args=(
            self.contract_dict['ErasurePosts'],
            self.w3.toBytes(hexstr=proofhash),
            self.w3.toBytes(hexstr=metadata)))
        create_feed_txn = self.feed_factory.functions.create(
            self.w3.toBytes(hexstr=initialize_feed_call_data))
        receipt = self.manage_transaction(create_feed_function)
        instance_created = self.feed_factory.events.InstanceCreated().processReceipt(receipt)
        logger.info(
            f"Feed created at address {instance_created[0]['args']['instance']}")
        return receipt

    def manage_transaction(self, function_call):
        # getting the gas price
        gas_price = self.w3.toWei(get_gas_price(), 'gwei')
        gas_estimated = function_call.estimateGas()
        gas_limit = 2*ceil(gas_estimated/1000.0)*1000
        unsigned_txn = function_call.buildTransaction({
            'chainId': self.w3.eth.chainId,
            'gasPrice': gas_price,
            'gas': 3*10**5,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
        })
        signed_txn = self.w3.eth.account.sign_transaction(
            create_feed_txn, self.account.key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        logger.info(f"Sent the transaction {tx_hash.hex()} to create feed")
        logger.info("Waiting for transaction to be mined ...")
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        instance_created = self.feed_factory.events.InstanceCreated().processReceipt(receipt)
        logger.info(
            f"Feed created at address {instance_created[0]['args']['instance']}")
        return receipt

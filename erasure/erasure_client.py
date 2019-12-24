import logging
import requests
from math import ceil
from erasure.contracts import (
    CONTRACTS
)
from erasure.session import initialize_erasure_account
from erasure.settings import (
    ERASURE_ACCOUNT_PRIVATE_KEY,
    ERASURE_KEY_STORE,
)
from erasure.utils import (
    initialize_contract,
)


logger = logging.getLogger(__name__)


class ErasureClient():
    """
    Main entrypoint for the erasuer python client
    """

    def __init__(self, w3, mode, version):
        self.w3 = w3
        self.mode = mode
        self.version = version
        self._key_store = ERASURE_KEY_STORE
        logger.info(f"Keys will be stored at {self._key_store}")
        self.account = initialize_erasure_account(
            w3, ERASURE_ACCOUNT_PRIVATE_KEY)
        # Initializing contract addresses
        if mode == 'rinkeby':
            logger.info(f"Connecting to Rinkeby testnet")
            assert w3.eth.chainId == 4
        elif mode == 'mainnet':
            logger.info(f"Connecting to ethereum mainnet")
            assert w3.eth.chainId == 1
        elif mode == 'test':
            logger.info(f"Running in test mode ignoring assertion")
        else:
            raise KeyError(f"Mode {mode} is not supported")
        logger.info(f"Running erasure client with {version} contracts")
        self.contract_dict = CONTRACTS[mode][version]
        # Initializing contracts
        self.feed_factory = initialize_contract(
            w3=self.w3,
            contract_address=self.contract_dict["FeedFactory"],
            contract_name="FeedFactory")
        self.feed_template = initialize_contract(
            w3=self.w3,
            contract_address=None,
            contract_name="Feed")
        self.erasure_users = initialize_contract(
            w3=self.w3,
            contract_address=self.contract_dict["ErasureUsers"],
            contract_name="ErasureUsers")

    def create_feed(self, operator, proofhash='0x', metadata='0x'):
        logger.info(f"Creating erasure with protocol version {self.version}")
        logger.info(
            f"Creating erasure feed for the user {self.account.address}")
        logger.info(
            f"Creating erasure feed at the operator {operator}")
        # get call data to create feed
        initialize_feed_call_data = self.feed_template.encodeABI('initialize', args=(
            operator,
            self.w3.toBytes(hexstr=proofhash),
            self.w3.toBytes(hexstr=metadata)))
        gas_price = self.get_gas_price()
        create_feed_function = self.feed_factory.functions.create(
            self.w3.toBytes(hexstr=initialize_feed_call_data)
        )
        gas_estimated = create_feed_function.estimateGas()
        gas_limit = 2*ceil(gas_estimated/1000.0)*1000
        receipt = self.manage_transaction(
            create_feed_function,
            gas_limit=gas_limit,
            gas_price=gas_price)
        instance_created = self.feed_factory.events.InstanceCreated().processReceipt(receipt)
        logger.info(
            f"Feed created at address {instance_created[0]['args']['instance']}")
        return receipt

    def create_user(self, public_key):
        logger.info(f"Registering user to the public key {public_key}")
        register_user_function = self.erasure_users.functions.registerUser(
            bytes(public_key, 'utf-8'))
        gas_price = self.get_gas_price()
        gas_estimated = register_user_function.estimateGas()
        gas_limit = 2*ceil(gas_estimated/1000.0)*1000
        receipt = self.manage_transaction(
            register_user_function,
            gas_limit=gas_limit,
            gas_price=gas_price)
        return receipt

    def manage_transaction(self, function_call, gas_limit, gas_price):
        unsigned_txn = function_call.buildTransaction({
            'chainId': self.w3.eth.chainId,
            'gasPrice': gas_price,
            'gas': gas_limit,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
        })
        signed_txn = self.w3.eth.account.sign_transaction(
            unsigned_txn, self.account.key)
        tx_hash = self.w3.eth.sendRawTransaction(
            signed_txn.rawTransaction)
        logger.info(f"Sent the transaction {tx_hash.hex()}")
        logger.info("Waiting for transaction to be mined ...")
        return self.w3.eth.waitForTransactionReceipt(tx_hash)

    def get_gas_price(self, mode='average'):
        if self.mode == 'test':
            return 0
        else:
            url = "https://ethgasstation.info/json/ethgasAPI.json"
            result = requests.get(url)
            return self.w3.toWei(result.json()[mode]/10, 'gwei')

    def update_key_store(self, new_key_store):
        self._key_store = new_key_store
        logger.info(f"Updated location of key store to {new_key_store}")

    def get_key_store(self):
        return self._key_store

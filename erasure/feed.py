import json
import logging
import multihash
from hashlib import sha256
from erasure.utils import (
    initialize_contract
)
from erasure.crypto import (
    generate_key,
    encrypt,
    multihash_sha256,
)

logger = logging.info(__name__)


class Feed():
    """
    Feed class to interact with the erasure feed
    """

    def __init__(self, erasure_client, feed_address):
        self.address = feed_address
        self.erasure_client = erasure_client
        self.contract = initialize_contract(
            w3=erasure_client.w3,
            contract_address=feed_address,
            contract_name="Feed")
        self.creator = self.contract.functions.getCreator().call()
        self.operator = self.contract.functions.getOperator().call()

    def create_post(self, raw_data, key=None):
        self.assert_client_is_connected_to_creator()
        if key is None:
            key = generate_key()
        json_proofhash_v120 = self.generate_proof_hash_json(raw_data, key)
        proof_hash_in_bytes = sha256(
            bytes(json_proofhash_v120, 'utf-8')).digest()
        submit_hash_function = self.contract.functions.submitHash(
            proof_hash_in_bytes)
        gas_price = self.erasure_client.get_gas_price()
        # estimate gas fails for some reason
        gas_limit = 100000
        receipt = self.erasure_client.manage_transaction(
            submit_hash_function,
            gas_limit=gas_limit,
            gas_price=gas_price)
        return receipt
        # TODO: save the key in ~/.erasure/proofhash (location)

    def generate_proof_hash_json(self, raw_data, key):
        encrypted_data = encrypt(key, raw_data)
        key_hash = multihash_sha256(key)
        data_hash = multihash_sha256(raw_data)
        encrypted_data_hash = multihash_sha256(encrypted_data)
        # constructing the json
        json_proofhash_v120 = json.dumps({
            "creator": self.creator,
            "datahash": data_hash,
            "keyhash": key_hash,
            "encryptedDatahash": encrypted_data_hash,
        })
        return json_proofhash_v120

    def assert_client_is_connected_to_creator(self):
        assert self.erasure_client.account.address == self.creator

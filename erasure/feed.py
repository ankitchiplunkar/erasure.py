import json
import logging
import multihash
from erasure.utils import (
    initialize_contract
)
from erasure.crypto import (
    generate_key,
    encrypt,
    multihash_sha3_256,
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
        proof_hash = self.erasure_client.w3.sha3(text=json_proofhash_v120)
        submit_hash_function = self.contract.functions.submitHash(bytes(proof_hash))
        receipt = self.erasure_client.manage_transaction(submit_hash_function)

    def generate_proof_hash(self, raw_data, key):
        encrypted_data = encrypt(key, raw_data)
        key_hash = multihash_sha3_256(key)
        data_hash = multihash_sha3_256(raw_data)
        encrypted_data_hash = multihash_sha3_256(encrypted_data)
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

import json
import logging
import multihash
from hashlib import sha256
from erasure.ipfs import (
    upload_bytes_to_ipfs,
)
from erasure.utils import (
    initialize_contract,
    write_file,
)
from erasure.crypto import (
    Symmetric,
    multihash_sha256,
)

logger = logging.getLogger(__name__)


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
        json_proofhash_v120, encrypted_data = self.generate_proof_hash_json(
            raw_data, key)
        proof_hash = sha256(
            bytes(json_proofhash_v120, 'utf-8'))
        submit_hash_function = self.contract.functions.submitHash(
            proof_hash.digest())
        gas_price = self.erasure_client.get_gas_price()
        # TODO: estimate gas fails for some reason
        gas_limit = 100000
        logger.info(
            f'Submitting proof hash {proof_hash.hexdigest()} to {self.erasure_client.mode} network')
        receipt = self.erasure_client.manage_transaction(
            submit_hash_function,
            gas_limit=gas_limit,
            gas_price=gas_price)
        logger.info(f"Uploading encrypted data to ipfs")
        cid = upload_bytes_to_ipfs(encrypted_data)
        self.save_post(key=key, encrypted_data=encrypted_data,
                       cid=cid, proof_hash=proof_hash)
        return receipt

    def generate_proof_hash_json(self, raw_data, key):
        encrypted_data = Symmetric.encrypt(key, raw_data)
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
        return json_proofhash_v120, encrypted_data

    def assert_client_is_connected_to_creator(self):
        assert self.erasure_client.account.address == self.creator

    def save_post(self, key, encrypted_data, cid, proof_hash):
        logger.info("Saving details of post locally")
        directory = f"{self.erasure_client._key_store}/{proof_hash.hexdigest()}"
        write_file(directory, "key", key)
        write_file(directory, "edata", encrypted_data)
        write_file(directory, "cid", cid)

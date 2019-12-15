import base58
import binascii
import logging
from ethpm._utils.ipfs import generate_file_hash
import ipfshttpclient

logger = logging.getLogger(__name__)


def hash_to_hex(hash_string):
    bytes_array = base58.b58decode(hash_string)
    b = bytes_array[2:]
    return "0x" + binascii.hexlify(b).decode("utf-8")


def get_ipfs_hash(input_data):
    return generate_file_hash(input_data)


def upload_bytes_to_ipfs(raw_data_in_bytes):
    assert isinstance(raw_data_in_bytes, bytes)
    with ipfshttpclient.connect() as client:
        cid = client.add_bytes(raw_data_in_bytes)
        logger.info(f"Upload successful to {cid}")
        return cid


def download_bytes_from_ipfs(cid):
    with ipfshttpclient.connect() as client:
        return client.cat(cid)

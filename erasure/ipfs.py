import base58
import binascii
from ethpm._utils.ipfs import generate_file_hash


def hash_to_hex(hash_string):
    bytes_array = base58.b58decode(hash_string)
    b = bytes_array[2:]
    return "0x" + binascii.hexlify(b).decode("utf-8")


def get_ipfs_hash(input_data):
    return generate_file_hash(input_data)

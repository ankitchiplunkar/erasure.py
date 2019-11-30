import base58
import binascii


def hash_to_hex(hash_string):
    bytes_array = base58.b58decode(hash_string)
    b = bytes_array[2:]
    return "0x" + binascii.hexlify(b).decode("utf-8")
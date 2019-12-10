from cryptography.fernet import Fernet
from multihash import Multihash
import hashlib


def generate_key():
    return Fernet.generate_key()


def encrypt(key, data_in_bytes):
    f = Fernet(key)
    if isinstance(data_in_bytes, bytes):
        return f.encrypt(data_in_bytes)


def decrypt(key, token):
    f = Fernet(key)
    return f.decrypt(token)


def multihash_sha3_256(data_in_bytes):
    hashed_data = hashlib.sha3_256(data_in_bytes)
    return Multihash.from_hash(hashed_data).encode("hex").decode('utf-8')
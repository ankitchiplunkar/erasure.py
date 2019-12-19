from cryptography.fernet import Fernet
from Crypto.PublicKey import ECC
import multihash


class Symmetric():
    @classmethod
    def generate_key(cls):
        return Fernet.generate_key()

    @classmethod
    def encrypt(cls, key, data_in_bytes):
        f = Fernet(key)
        if isinstance(data_in_bytes, bytes):
            return f.encrypt(data_in_bytes)

    @classmethod
    def decrypt(cls, key, token):
        f = Fernet(key)
        return f.decrypt(token)


def multihash_sha256(data_in_bytes):
    return multihash.digest(data_in_bytes, "sha2_256").encode("hex").decode('utf-8')

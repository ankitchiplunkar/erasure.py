from cryptography.fernet import Fernet
import multihash


def generate_key():
    return Fernet.generate_key()


def encrypt(key, data_in_bytes):
    f = Fernet(key)
    if isinstance(data_in_bytes, bytes):
        return f.encrypt(data_in_bytes)


def decrypt(key, token):
    f = Fernet(key)
    return f.decrypt(token)


def multihash_sha256(data_in_bytes):
    return multihash.digest(data_in_bytes, "sha2_256").encode("hex").decode('utf-8')

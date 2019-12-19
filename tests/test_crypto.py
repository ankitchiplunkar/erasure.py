from cryptography.fernet import InvalidToken
from erasure.crypto import (
    Symmetric,
    multihash_sha256,
)
import pytest


def test_symmetric_generate_key():
    assert len(Symmetric.generate_key()) == 44


def test_symmetric_encrypt_decrypt_data():
    key1 = Symmetric.generate_key()
    key2 = Symmetric.generate_key()
    msg = b"this is a message"
    encrypted_message = Symmetric.encrypt(key1, msg)
    decrypted_message = Symmetric.decrypt(key1, encrypted_message)
    assert msg == decrypted_message
    with pytest.raises(InvalidToken):
        assert msg == Symmetric.decrypt(key2, encrypted_message)


def test_multihash_sha256():
    data_in_bytes = bytes("multihash", "utf-8")
    multihashformat = multihash_sha256(data_in_bytes)
    assert "12209cbc07c3f991725836a3aa2a581ca2029198aa420b9d99bc0e131d9f3e2cbe47" == multihashformat

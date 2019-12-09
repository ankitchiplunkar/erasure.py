from cryptography.fernet import InvalidToken
from erasure.crypto import (
    generate_key,
    encrypt,
    decrypt,
    multihash_sha3_256,
)
import pytest


def test_symmetric_generate_key():
    assert len(generate_key()) == 44


def test_symmetric_encrypt_decrypt_data():
    key1 = generate_key()
    key2 = generate_key()
    msg = b"this is a message"
    encrypted_message = encrypt(key1, msg)
    decrypted_message = decrypt(key1, encrypted_message)
    assert msg == decrypted_message
    with pytest.raises(InvalidToken):
        assert msg == decrypt(key2, encrypted_message)


def test_multihash_sha256():
    data_in_bytes = bytes("multihash", "utf-8")
    multihashformat = multihash_sha3_256(data_in_bytes)
    assert "162008c3792b2a4deed1bd7ea2328fb5de5531eccf0fbfa04a7d800cdc267137c635" == multihashformat

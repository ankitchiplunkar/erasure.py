from cryptography.fernet import InvalidToken
from erasure.crypto import (
    generate_key,
    encrypt,
    decrypt,
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

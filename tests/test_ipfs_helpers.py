import pytest
from erasure.ipfs import (
    get_ipfs_hash,
    hash_to_hex,
    upload_bytes_to_ipfs,
    download_bytes_from_ipfs,
)
from tests.common import (
    setup_ipfs_daemon
)

input_data = "Hello World!\n".encode()
ipfs_cid = "QmfM2r8seH2GiRaC4esTjeraXEachRt8ZsSeGaWTPLyMoG"


def test_hash_to_hex():
    "should convert a b58 ipfs hash to to hex with 0x prefix"
    hex_string = "0x227e75ab3fb8ba90fbb7addb3d30bd20c676f873e0216a767084b2073e0b7d9f"
    hash_string = "QmQfJQtxGA5MzWi5HZPyCaZiPAzNkxq8U9yApihkKsWZx2"
    assert hash_to_hex(hash_string) == hex_string


def test_ipfs_hash():
    assert get_ipfs_hash(input_data) == ipfs_cid


def test_upload_download(setup_ipfs_daemon):
    assert upload_bytes_to_ipfs(input_data) == ipfs_cid
    assert download_bytes_from_ipfs(ipfs_cid) == input_data

from erasure.ipfs import hash_to_hex


def test_ipfs_hash_to_hex():
    "should convert a b58 ipfs hash to to hex with 0x prefix"
    hex_string = "0x227e75ab3fb8ba90fbb7addb3d30bd20c676f873e0216a767084b2073e0b7d9f"
    hash_string = "QmQfJQtxGA5MzWi5HZPyCaZiPAzNkxq8U9yApihkKsWZx2"
    assert hash_to_hex(hash_string) == hex_string
    
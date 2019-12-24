from tests.common import (
    init_feed,
    init_erasure_client,
    raw_data,
    key,
)
from erasure.post import Post
from erasure.ipfs import download_bytes_from_ipfs
from erasure.crypto import decrypt


def test_reveal(init_feed):
    receipt = init_feed.create_post(raw_data, key=key)
    hash_submitted = init_feed.contract.events.HashSubmitted().processReceipt(receipt)
    proof_hash_hex = init_feed.erasure_client.w3.toHex(
        hash_submitted[0]['args']['hash'])
    post = Post(init_feed, proof_hash_hex[2:])
    key_cid, data_cid = post.reveal()
    post._fetch_post_secrets()
    data = decrypt(post.key, post.encrypted_data)
    assert post.key == download_bytes_from_ipfs(key_cid)
    assert data == download_bytes_from_ipfs(data_cid)

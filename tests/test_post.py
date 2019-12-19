from tests.common import (
    feed,
    raw_data,
    key,
)
from erasure.post import Post
from erasure.ipfs import download_bytes_from_ipfs
from erasure.crypto import Symmetric

receipt = feed.create_post(raw_data, key=key)


def test_reveal():
    hash_submitted = feed.contract.events.HashSubmitted().processReceipt(receipt)
    proof_hash_hex = feed.erasure_client.w3.toHex(
        hash_submitted[0]['args']['hash'])
    post = Post(feed, proof_hash_hex[2:])
    key_cid, data_cid = post.reveal()
    post._fetch_post_secrets()
    data = Symmetric.decrypt(post.key, post.encrypted_data)
    assert post.key == download_bytes_from_ipfs(key_cid)
    assert data == download_bytes_from_ipfs(data_cid)

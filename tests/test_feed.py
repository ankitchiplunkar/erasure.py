import json
from hashlib import sha256
import pytest
from tests.common import (
    init_erasure_client,
    init_feed,
    raw_data,
    key,
    test_operator,
    setup_erasure_test_env,
    setup_ipfs_daemon,
)
from erasure.feed import Feed
from erasure.utils import get_file_contents
from erasure.crypto import (
    Symmetric,
    multihash_sha256,
)
from erasure.ipfs import download_bytes_from_ipfs
from erasure.post import Post


def test_init_feed(setup_erasure_test_env, init_erasure_client, init_feed):
    assert init_feed.creator == init_erasure_client.account.address
    assert init_feed.operator == test_operator


def test_assert_client_is_connected_to_creator(setup_erasure_test_env, init_feed):
    init_feed.assert_client_is_connected_to_creator()


def test_generate_proof_hash_json(setup_erasure_test_env, init_feed):
    json_proofhash_v120, encrypted_data = init_feed.generate_proof_hash_json(
        raw_data, key)
    dict_proofhash = json.loads(json_proofhash_v120)
    assert dict_proofhash['creator'] == init_feed.creator
    assert dict_proofhash['keyhash'] == "12207cc1aecef100afce425b7ea2eabd791eafec252c0e7be07dcf2ab911c4ee19d6"
    assert dict_proofhash['datahash'] == "12209cbc07c3f991725836a3aa2a581ca2029198aa420b9d99bc0e131d9f3e2cbe47"


@pytest.mark.xfail(reason='ipfs tests are flaky in travis ci')
def test_create_post(setup_erasure_test_env, setup_ipfs_daemon, init_feed):
    receipt = init_feed.create_post(raw_data, key=key)
    hash_submitted = init_feed.contract.events.HashSubmitted().processReceipt(receipt)
    proof_hash_hex = init_feed.erasure_client.w3.toHex(
        hash_submitted[0]['args']['hash'])
    post = Post(init_feed, proof_hash_hex[2:])
    post._fetch_post_secrets()
    assert post.key == key
    assert post.encrypted_data == download_bytes_from_ipfs(post.cid)
    data = Symmetric.decrypt(post.key, post.encrypted_data)
    key_hash = multihash_sha256(post.key)
    data_hash = multihash_sha256(data)
    encrypted_data_hash = multihash_sha256(post.encrypted_data)
    # asserting the proof hash json
    json_proofhash_v120 = json.dumps({
        "creator": init_feed.creator,
        "datahash": data_hash,
        "keyhash": key_hash,
        "encryptedDatahash": encrypted_data_hash,
    })
    proof_hash = sha256(
        bytes(json_proofhash_v120, 'utf-8'))
    assert proof_hash_hex[2:] == proof_hash.hexdigest()

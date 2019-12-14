import json
from hashlib import sha256
from tests.common import erasure_client
from erasure.feed import Feed
from erasure.utils import get_file_contents
from erasure.crypto import (
    decrypt,
    multihash_sha256,
)
from erasure.ipfs import download_bytes_from_ipfs

FEED_ADDRESS = "0xd7b553e28c101B6fA6ae2f7824c9f78f8fDC13B7"
raw_data = bytes("multihash", "utf-8")
key = b'B1yfUQ64D86WaumL1vjm1Ua7-7j0_YjjdOlsA-y9bQo='


def create_feed():
    return Feed(erasure_client=erasure_client, feed_address=FEED_ADDRESS)


def test_init_feed():
    feed = create_feed()
    assert feed.creator == erasure_client.account.address
    assert feed.operator == erasure_client.contract_dict["ErasurePosts"]


def test_assert_client_is_connected_to_creator():
    feed = create_feed()
    feed.assert_client_is_connected_to_creator()


def test_generate_proof_hash_json():
    feed = create_feed()
    json_proofhash_v120, encrypted_data = feed.generate_proof_hash_json(
        raw_data, key)
    dict_proofhash = json.loads(json_proofhash_v120)
    assert dict_proofhash['creator'] == feed.creator
    assert dict_proofhash['keyhash'] == "12207cc1aecef100afce425b7ea2eabd791eafec252c0e7be07dcf2ab911c4ee19d6"
    assert dict_proofhash['datahash'] == "12209cbc07c3f991725836a3aa2a581ca2029198aa420b9d99bc0e131d9f3e2cbe47"


def test_create_post():
    feed = create_feed()
    receipt = feed.create_post(raw_data, key=key)
    hash_submitted = feed.contract.events.HashSubmitted().processReceipt(receipt)
    proof_hash_hex = feed.erasure_client.w3.toHex(
        hash_submitted[0]['args']['hash'])
    key_store = feed.erasure_client.get_key_store()
    retrieved_key = get_file_contents(f"{key_store}/{proof_hash_hex[2:]}/key").encode('utf-8')
    encrypted_data = get_file_contents(
        f"{key_store}/{proof_hash_hex[2:]}/edata").encode('utf-8')
    cid = get_file_contents(f"{key_store}/{proof_hash_hex[2:]}/cid")
    assert retrieved_key == key
    assert encrypted_data == download_bytes_from_ipfs(cid)
    data = decrypt(retrieved_key, encrypted_data)
    key_hash = multihash_sha256(key)
    data_hash = multihash_sha256(data)
    encrypted_data_hash = multihash_sha256(encrypted_data)
    # asserting the proof hash json
    json_proofhash_v120 = json.dumps({
        "creator": feed.creator,
        "datahash": data_hash,
        "keyhash": key_hash,
        "encryptedDatahash": encrypted_data_hash,
    })
    proof_hash = sha256(
        bytes(json_proofhash_v120, 'utf-8'))
    assert proof_hash_hex[2:] == proof_hash.hexdigest()

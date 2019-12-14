import json
from hashlib import sha256
from tests.common import erasure_client
from erasure.feed import Feed

FEED_ADDRESS = "0xd7b553e28c101B6fA6ae2f7824c9f78f8fDC13B7"
key = b'B1yfUQ64D86WaumL1vjm1Ua7-7j0_YjjdOlsA-y9bQo='
raw_data = bytes("multihash", "utf-8")


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
    json_proofhash_v120 = feed.generate_proof_hash_json(raw_data, key)
    dict_proofhash = json.loads(json_proofhash_v120)
    assert dict_proofhash['creator'] == feed.creator
    assert dict_proofhash['keyhash'] == "12207cc1aecef100afce425b7ea2eabd791eafec252c0e7be07dcf2ab911c4ee19d6"
    assert dict_proofhash['datahash'] == "12209cbc07c3f991725836a3aa2a581ca2029198aa420b9d99bc0e131d9f3e2cbe47"


def test_create_post():
    feed = create_feed()
    receipt = feed.create_post(raw_data, key=key)
    hash_submitted = feed.contract.events.HashSubmitted().processReceipt(receipt)
    # cannot check for hash submitted right now because fernet has a time
    # component and fernet hash varies with time
    assert hash_submitted[0]['event'] == 'HashSubmitted'

import json
from tests.common import erasure_client
from erasure.feed import Feed

FEED_ADDRESS = "0xd7b553e28c101B6fA6ae2f7824c9f78f8fDC13B7"
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
    raw_data = bytes("multihash", "utf-8")
    json_proofhash_v120 = feed.generate_proof_hash_json(raw_data, key)
    dict_proofhash = json.loads(json_proofhash_v120)
    assert dict_proofhash['creator'] == feed.creator
    assert dict_proofhash['keyhash'] == "1620462ec6f428569034c407b5e8dd2d7c0f46dd2f5ce55897a78aff0ec8d5cf9727"
    assert dict_proofhash['datahash'] == "162008c3792b2a4deed1bd7ea2328fb5de5531eccf0fbfa04a7d800cdc267137c635"
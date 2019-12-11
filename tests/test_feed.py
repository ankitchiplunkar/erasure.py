import json
from tests.common import erasure_client
from erasure.feed import Feed

FEED_ADDRESS = "0x2567e4b9e586128683046121943431267b412153"
feed = Feed(erasure_client=erasure_client, feed_address=FEED_ADDRESS)
key = b'B1yfUQ64D86WaumL1vjm1Ua7-7j0_YjjdOlsA-y9bQo='


def test_init_feed():
    assert feed.creator == erasure_client.account.address
    assert feed.operator == erasure_client.contract_dict["ErasurePosts"]


def test_assert_client_is_connected_to_creator():
    feed.assert_client_is_connected_to_creator()


def test_generate_proof_hash_json():
    raw_data = bytes("multihash", "utf-8")
    json_proofhash_v120 = feed.generate_proof_hash_json(raw_data, key)
    dict_proofhash = json.loads(json_proofhash_v120)
    assert dict_proofhash['creator'] == feed.creator
    assert dict_proofhash['keyhash'] == "12207cc1aecef100afce425b7ea2eabd791eafec252c0e7be07dcf2ab911c4ee19d6"
    assert dict_proofhash['datahash'] == "12209cbc07c3f991725836a3aa2a581ca2029198aa420b9d99bc0e131d9f3e2cbe47"

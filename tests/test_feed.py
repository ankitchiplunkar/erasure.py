from tests.common import erasure_client
from erasure.feed import Feed

FEED_ADDRESS = "0x2567e4b9e586128683046121943431267b412153"


def test_init_feed():
    feed = Feed(erasure_client=erasure_client, feed_address=FEED_ADDRESS)
    assert feed.creator == erasure_client.account.address
    assert feed.operator == erasure_client.contract_dict["ErasurePosts"]

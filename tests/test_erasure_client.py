from erasure.session import (
    setup_logging,
    init_web3,
    initialize_erasure_account
)
from erasure.settings import (
    ERASURE_NODE_URL,
    ERASURE_ACCOUNT_PRIVATE_KEY,
)
from erasure.erasure_client import ErasureClient


mode = "rinkeby"
version = "v1.2.0"
setup_logging()
w3 = init_web3(node_url=ERASURE_NODE_URL)
erasure_client = ErasureClient(w3, mode, version)


def test_create_feed():
    receipt = erasure_client.create_feed()
    instance_created = erasure_client.feed_factory.events.InstanceCreated().processReceipt(receipt)
    assert instance_created[0]['args']['creator'] == erasure_client.account.address
    feed_initialized = erasure_client.feed.events.Initialized().processReceipt(receipt)
    assert feed_initialized[0]['args']['operator'] == erasure_client.contract_dict['ErasurePosts']



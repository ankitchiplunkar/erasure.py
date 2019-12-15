from erasure.session import (
    setup_logging,
    init_web3,
    initialize_erasure_account
)
from erasure.settings import (
    ERASURE_ACCOUNT_PRIVATE_KEY,
)
from erasure.erasure_client import ErasureClient
from erasure.feed import Feed

# Initialize test variables
mode = "test"
version = "v1.2.0"
setup_logging()
ERASURE_NODE_URL = 'http://localhost:8545'
raw_data = bytes("multihash", "utf-8")
key = b'B1yfUQ64D86WaumL1vjm1Ua7-7j0_YjjdOlsA-y9bQo='
test_operator="0x0000000000000000000000000000000000000000"
# Initializing erasure client
w3 = init_web3(node_url=ERASURE_NODE_URL)
erasure_client = ErasureClient(w3, mode, version)
erasure_client.update_key_store('/tmp')
# Initializing feed
receipt = erasure_client.create_feed(operator=test_operator)
FEED_ADDRESS = "0xf99196ec2c2b15b625FF1707a98458b2CfE3e554"
feed = Feed(erasure_client=erasure_client, feed_address=FEED_ADDRESS)

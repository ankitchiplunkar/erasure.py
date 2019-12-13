from erasure.session import (
    setup_logging,
    init_web3,
    initialize_erasure_account
)
from erasure.settings import (
    ERASURE_ACCOUNT_PRIVATE_KEY,
)
from erasure.erasure_client import ErasureClient


mode = "test"
version = "v1.2.0"
setup_logging()
ERASURE_NODE_URL = 'http://localhost:8545'
w3 = init_web3(node_url=ERASURE_NODE_URL)
erasure_client = ErasureClient(w3, mode, version)

from erasure.session import (
    setup_logging,
    init_web3,
    initialize_erasure_account
)
from erasure.settings import (
    ERASURE_NODE_URL,
    ERASURE_ACCOUNT_PRIVATE_KEY,
    ERASURE_MODE,
)
from erasure.erasure_client import ErasureClient


version = "v1.0.0"
setup_logging()
w3 = init_web3(node_url=ERASURE_NODE_URL)



def test_init_erasure_client():
    erasure_client = ErasureClient(w3, ERASURE_MODE, version)
    pass
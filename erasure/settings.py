import os

HOME_DIR = os.path.expanduser("~")

# Logging settings
LOG_STDOUT = os.getenv("LOG_STDOUT", "TRUE")
LOG_FORMAT = os.getenv(
    "LOG_FORMAT", "[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Connection settings
ERASURE_NODE_URL = os.getenv("ERASURE_NODE_URL", "http://127.0.0.1:8545")
ERASURE_MODE = os.getenv("ERASURE_MODE", "rinkeby")
GAS_PRICE_MODE = os.getenv("GAS_PRICE_MODE", "average")

# Address settings
TEST_PRIVATE_KEY = '0x6a8b4de52b288e111c14e1c4b868bc125d325d40331d86d875a3467dd44bf829'
ERASURE_ACCOUNT_PRIVATE_KEY = os.getenv(
    "ERASURE_ACCOUNT_PRIVATE_KEY", TEST_PRIVATE_KEY)
FEED_CONTRACT_ADDRESS = os.getenv("FEED_CONTRACT_ADDRESS")
ERASURE_KEY_STORE = os.getenv("ERASURE_KEY_STORE", f"{HOME_DIR}/.erasure/")

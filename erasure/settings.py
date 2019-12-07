import os

# Logging settings
LOG_STDOUT = os.getenv("LOG_STDOUT", "TRUE")
LOG_FORMAT = os.getenv(
    "LOG_FORMAT", "[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Connection settings
ERASURE_NODE_URL = os.getenv("ERASURE_NODE_URL")

# Address settings
TEST_PRIVATE_KEY = '0x6a8b4de52b288e111c14e1c4b868bc125d325d40331d86d875a3467dd44bf829'
ERASURE_ACCOUNT_PRIVATE_KEY = os.getenv("ERASURE_ACCOUNT_PRIVATE_KEY", TEST_PRIVATE_KEY)
FEED_CONTRACT_ADDRESS = os.getenv("FEED_CONTRACT_ADDRESS")
ERASURE_PROTOCOL_VERSION = os.getenv("ERASURE_PROTOCOL_VERSION", "0.1.1")

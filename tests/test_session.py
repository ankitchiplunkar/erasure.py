from erasure.session import initialize_erasure_account
from web3.auto import w3
from erasure.settings import TEST_PRIVATE_KEY


def test_account():
    account = initialize_erasure_account(w3, TEST_PRIVATE_KEY)
    assert account.address == "0x634743b15C948820069a43f6B361D03EfbBBE5a8"

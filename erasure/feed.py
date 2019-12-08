import logging
from erasure.utils import (
    initialize_contract
)

logger = logging.info(__name__)



class Feed():
    """
    Feed class to interact with the erasure feed
    """

    def __init__(self, erasure_client, feed_address):
        self.address = feed_address
        self.contract = initialize_contract(
            w3=erasure_client.w3,
            contract_address=feed_address,
            contract_name="Feed")
        self.creator = self.contract.functions.getCreator().call()
        self.operator = self.contract.functions.getOperator().call()
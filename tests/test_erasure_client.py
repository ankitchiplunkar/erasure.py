import pytest
from tests.common import erasure_client


@pytest.mark.skip(reason="Takes too much time")
def test_create_feed():
    receipt = erasure_client.create_feed()
    instance_created = erasure_client.feed_factory.events.InstanceCreated().processReceipt(receipt)
    assert instance_created[0]['args']['creator'] == erasure_client.account.address
    feed_initialized = erasure_client.feed_template.events.Initialized().processReceipt(receipt)
    assert feed_initialized[0]['args']['operator'] == erasure_client.contract_dict['ErasurePosts']

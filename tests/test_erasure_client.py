from tests.common import (
    erasure_client,
    test_operator,
)


def test_create_feed():
    receipt = erasure_client.create_feed(operator=test_operator)
    instance_created = erasure_client.feed_factory.events.InstanceCreated().processReceipt(receipt)
    assert instance_created[0]['args']['creator'] == erasure_client.account.address
    feed_initialized = erasure_client.feed_template.events.Initialized().processReceipt(receipt)
    assert feed_initialized[0]['args']['operator'] == test_operator

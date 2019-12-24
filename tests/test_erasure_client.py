from tests.common import (
    init_erasure_client,
    test_operator,
)


def test_create_feed(init_erasure_client):
    receipt = init_erasure_client.create_feed(operator=test_operator)
    instance_created = init_erasure_client.feed_factory.events.InstanceCreated().processReceipt(receipt)
    assert instance_created[0]['args']['creator'] == init_erasure_client.account.address
    feed_initialized = init_erasure_client.feed_template.events.Initialized().processReceipt(receipt)
    assert feed_initialized[0]['args']['operator'] == test_operator

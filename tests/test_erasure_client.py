from tests.common import (
    init_erasure_client,
    setup_erasure_test_env,
    test_operator,
)


def test_create_feed(setup_erasure_test_env, init_erasure_client):
    receipt = init_erasure_client.create_feed(operator=test_operator)
    instance_created = init_erasure_client.feed_factory.events.InstanceCreated(
    ).processReceipt(receipt)
    assert instance_created[0]['args']['creator'] == init_erasure_client.account.address
    feed_initialized = init_erasure_client.feed_template.events.Initialized(
    ).processReceipt(receipt)
    assert feed_initialized[0]['args']['operator'] == test_operator


def test_create_user(setup_erasure_test_env, init_erasure_client):
    receipt = init_erasure_client.create_user(public_key=test_operator)
    user_registered = init_erasure_client.erasure_users.events.UserRegistered(
    ).processReceipt(receipt)
    assert user_registered[0]['args']['user'] == init_erasure_client.account.address
    assert user_registered[0]['args']['data'] == bytes(test_operator, 'utf-8')

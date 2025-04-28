from ansible_aap_api_client.schemas import (
    InventoryRequestSchema,
    InventoryHostRequestSchema,
    InventoryGroupRequestSchema,
)


def test_inventory_request_schema():
    obj = InventoryRequestSchema(name="test", description="test", organization=1)


def test_inventory_host_request_schema():
    obj = InventoryHostRequestSchema(name="test", description="test")


def test_inventory_group_request_schema():
    obj = InventoryGroupRequestSchema(name="test", description="test")

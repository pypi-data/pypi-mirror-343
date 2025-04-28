import pytest
from ansible_aap_api_client import Inventory, InventoryRequestSchema


def test_create_inventory(requests_create_inventory, inventory_request_schema):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    response = inventory.create_inventory(inventory=inventory_request_schema)


def test_create_inventory_bad(requests_create_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        inventory.create_inventory(inventory="bad")


def test_get_all_inventories(requests_get_two_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    response = inventory.get_all_inventories()


def test_get_inventory(requests_get_single_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    response = inventory.get_inventory(name="Demo Inventory")


def test_get_inventory_bad(requests_get_single_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        inventory.get_inventory(name=1)


def test_get_inventory_id(requests_get_single_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    response = inventory.get_inventory_id(name="Demo Inventory")

    assert response == 1


def test_get_inventory_id_bad(requests_get_two_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(ValueError):
        inventory.get_inventory_id(name="Demo Inventory")

    with pytest.raises(TypeError):
        inventory.get_inventory_id(name=1)


def test_add_host_to_inventory(requests_add_host_inventory, inventory_host_request_schema):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    response = inventory.add_host_to_inventory(inventory_id=38, host=inventory_host_request_schema)


def test_add_host_to_inventory_bad(requests_add_host_inventory, inventory_host_request_schema):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        inventory.add_host_to_inventory(inventory_id=38, host="bad")

    with pytest.raises(TypeError):
        inventory.add_host_to_inventory(inventory_id="bad", host=inventory_host_request_schema)


def test_add_group_to_inventory(requests_add_group_inventory, inventory_group_request_schema):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    response = inventory.add_group_to_inventory(inventory_id=38, group=inventory_group_request_schema)


def test_add_group_to_inventory_bad(requests_add_group_inventory, inventory_group_request_schema):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        inventory.add_group_to_inventory(inventory_id=38, group="bad")

    with pytest.raises(TypeError):
        inventory.add_group_to_inventory(inventory_id="bad", group=inventory_group_request_schema)


def test_delete_inventory(requests_delete_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    response = inventory.delete_inventory(inventory_id=2)


def test_delete_inventory_bad(requests_delete_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        inventory.delete_inventory(inventory_id="bad")


def test_update_inventory_bad(requests_delete_inventory):
    inventory = Inventory(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        inventory.update_inventory(inventory_id="bad", inventory="bad")

    with pytest.raises(TypeError):
        inventory.update_inventory(inventory_id=2, inventory="bad")

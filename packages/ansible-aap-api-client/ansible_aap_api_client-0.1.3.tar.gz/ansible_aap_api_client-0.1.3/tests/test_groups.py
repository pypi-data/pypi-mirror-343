import pytest
from ansible_aap_api_client import Group


def test_get_all_groups(requests_get_two_group):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    response = obj.get_all_groups()


def test_get_group(requests_get_two_group):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    obj.get_group(name="test_group")


def test_get_group_bad(requests_get_two_group):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.get_group(name=1)


def test_get_group_id(requests_get_single_group):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    response = obj.get_group_id(name="test_group")

    assert response == 2


def test_get_group_id_bad(requests_get_two_group):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(ValueError):
        obj.get_group_id(name="test_group")

    with pytest.raises(TypeError):
        obj.get_group_id(name=1)


def test_add_host_to_group(requests_add_host_group, inventory_host_request_schema):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    response = obj.add_host_to_group(group_id=2, host=inventory_host_request_schema)


def test_add_host_to_group_bad(requests_add_host_group, inventory_host_request_schema):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.add_host_to_group(group_id=2, host="bad")

    with pytest.raises(TypeError):
        obj.add_host_to_group(group_id="bad", host=inventory_host_request_schema)


def test_delete_group(requests_delete_group):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    response = obj.delete_group(group_id=2)


def test_delete_group_bad(requests_delete_group):
    obj = Group(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.delete_group(group_id="bad")

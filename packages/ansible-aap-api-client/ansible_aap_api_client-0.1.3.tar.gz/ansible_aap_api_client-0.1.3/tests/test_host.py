import pytest
from ansible_aap_api_client import Host


def test_get_all_hosts(requests_get_two_host):
    obj = Host(base_url="https://localhost:5000", username="test", password="test")
    response = obj.get_all_hosts()


def test_get_host(requests_get_two_host):
    obj = Host(base_url="https://localhost:5000", username="test", password="test")
    obj.get_host(name="test_host")


def test_get_host_bad(requests_get_two_host):
    obj = Host(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.get_host(name=1)


def test_get_host_id(requests_get_single_host):
    obj = Host(base_url="https://localhost:5000", username="test", password="test")
    response = obj.get_host_id(name="test_host")

    assert response == 1


def test_get_host_id_bad(requests_get_two_host):
    obj = Host(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(ValueError):
        obj.get_host_id(name="test_host")

    with pytest.raises(TypeError):
        obj.get_host_id(name=1)


def test_delete_host(requests_delete_host):
    obj = Host(base_url="https://localhost:5000", username="test", password="test")
    response = obj.delete_host(host_id=2)


def test_delete_host_bad(requests_delete_host):
    obj = Host(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.delete_host(host_id="bad")


def test_update_host_bad(requests_delete_host):
    obj = Host(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.update_host(host_id="bad", host="bad")

    with pytest.raises(TypeError):
        obj.update_host(host_id=2, host="bad")

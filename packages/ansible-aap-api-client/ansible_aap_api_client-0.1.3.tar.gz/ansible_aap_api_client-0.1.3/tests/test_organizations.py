import pytest
from ansible_aap_api_client import Organization


def test_get_all_organizations(requests_get_two_organization):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    obj.get_all_organizations()


def test_get_organization(requests_get_two_organization):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    obj.get_organization(name="Default")


def test_get_organization_bad(requests_get_two_organization):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.get_organization(name=1)


def test_get_organization_id(requests_get_single_organization):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    obj.get_organization_id(name="Default")


def test_get_organization_id_bad(requests_get_two_organization):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(ValueError):
        obj.get_organization_id(name="Default")

    with pytest.raises(TypeError):
        obj.get_organization_id(name=1)


def test_delete_organization(requests_delete_organization):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    obj.delete_organization(organization_id=1)


def test_delete_organization_bad(requests_delete_organization):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.delete_organization(organization_id="bad")


def test_create_organization(requests_create_organization, organization_request_schema):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    obj.create_organization(organization=organization_request_schema)


def test_create_organization_bad(requests_create_organization, organization_request_schema):
    obj = Organization(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.create_organization(organization="bad")

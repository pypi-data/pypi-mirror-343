import pytest
from ansible_aap_api_client import JobManagement


def test_run_job(requests_get_singe_job_template, requests_get_single_inventory, requests_job_template_job_launch):
    job_management = JobManagement(
        base_url="https://localhost:5000",
        username="test",
        password="test",
        ssl_verify=False,
        job_template_name="Demo Job Template",
        inventory_name="Demo Inventory",
    )

    job_management.run()


def test_run_job_bad():
    with pytest.raises(TypeError):
        job_management = JobManagement(
            base_url="https://localhost:5000",
            username="test",
            password="test",
            ssl_verify=False,
            job_template_name=1,
            inventory_name="Demo Inventory",
        )

    with pytest.raises(TypeError):
        job_management = JobManagement(
            base_url="https://localhost:5000",
            username="test",
            password="test",
            ssl_verify=False,
            job_template_name="Demo Job Template",
            inventory_name=1,
        )

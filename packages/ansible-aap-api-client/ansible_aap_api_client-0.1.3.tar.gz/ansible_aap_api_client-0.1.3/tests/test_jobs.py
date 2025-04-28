import pytest
from ansible_aap_api_client import Job


def test_get_job(requests_single_job):
    obj = Job(base_url="https://localhost:5000", username="test", password="test")
    obj.get_job(job_id=35)


def test_get_job_bad(requests_single_job):
    obj = Job(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.get_job(job_id="bad")


def test_get_job_stdout(requests_job_stdout):
    obj = Job(base_url="https://localhost:5000", username="test", password="test")
    obj.get_job_stdout(job_id=35, output_format="txt")


def test_get_job_stdout_bad(requests_job_stdout):
    obj = Job(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.get_job_stdout(job_id="bad", output_format="txt")


def test_get_job_status(requests_single_job):
    obj = Job(base_url="https://localhost:5000", username="test", password="test")
    obj.get_job_status(job_id=35)


def test_get_job_status_bad(requests_single_job):
    obj = Job(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.get_job_status(job_id="bad")

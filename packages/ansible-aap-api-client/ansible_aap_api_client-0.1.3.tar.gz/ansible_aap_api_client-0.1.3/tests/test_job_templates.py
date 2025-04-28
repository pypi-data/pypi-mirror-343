import pytest
from ansible_aap_api_client import JobTemplate


def test_get_all_job_templates(requests_get_two_job_template):
    obj = JobTemplate(base_url="https://localhost:5000", username="test", password="test")
    obj.get_all_job_templates()


def test_get_job_template(requests_get_singe_job_template):
    obj = JobTemplate(base_url="https://localhost:5000", username="test", password="test")
    obj.get_job_template(name="Demo Job Template")


def test_get_job_template_bad(requests_get_singe_job_template):
    obj = JobTemplate(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.get_job_template(name=1)


def test_get_job_template_id(requests_get_singe_job_template):
    obj = JobTemplate(base_url="https://localhost:5000", username="test", password="test")
    obj.get_job_template_id(name="Demo Job Template")


def test_get_job_template_id_bad(requests_get_two_job_template):
    obj = JobTemplate(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(ValueError):
        obj.get_job_template_id(name="Demo Job Template")

    with pytest.raises(TypeError):
        obj.get_job_template_id(name=1)


def test_launch_job_template(requests_job_template_job_launch):
    obj = JobTemplate(base_url="https://localhost:5000", username="test", password="test")
    obj.launch_job_template(job_template_id=7)


def test_launch_job_template_bad(requests_job_template_job_launch):
    obj = JobTemplate(base_url="https://localhost:5000", username="test", password="test")
    with pytest.raises(TypeError):
        obj.launch_job_template(job_template_id="bad")

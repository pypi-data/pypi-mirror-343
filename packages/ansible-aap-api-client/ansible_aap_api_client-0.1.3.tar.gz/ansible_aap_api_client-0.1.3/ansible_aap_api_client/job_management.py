"""
AAP Job Management
"""

from typing import Optional, Union
import time
from ansible_aap_api_client.inventory_management import InventoryManagement
from ansible_aap_api_client.job_templates import JobTemplate
from ansible_aap_api_client.jobs import Job
from ansible_aap_api_client.interfaces.runable import Runable


class JobManagement(Runable, InventoryManagement, JobTemplate, Job):  # pylint: disable=too-many-ancestors
    """Job management class, to run a job template against an inventory

    :type base_url: str
    :param base_url: The base url to use
    :type username: str
    :param username: The username to use
    :type password: str
    :param password: The password to use
    :type ssl_verify: Union[bool, str]
    :param ssl_verify: The SSL verification True or False or a path to a certificate
    :type job_template_name: str
    :param job_template_name: The name of the job template
    :type inventory_name: str
    :param inventory_name: The name of the inventory

    :raises TypeError: If job_template_name is not of type str
    :raises TypeError: If inventory_name is not of type str
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        base_url: str,
        username: str,
        password: str,
        ssl_verify: Union[bool, str],
        job_template_name: str,
        inventory_name: str,
    ) -> None:
        super().__init__(base_url=base_url, username=username, password=password, ssl_verify=ssl_verify)

        if not isinstance(job_template_name, str):
            raise TypeError(f"job_template_name must be of type str, but received {type(job_template_name)}")

        if not isinstance(inventory_name, str):
            raise TypeError(f"inventory_name must be of type str, but received {type(inventory_name)}")

        self.job_template_name = job_template_name
        self.job_template_id = None
        self.inventory_name = inventory_name
        self.inventory_id = None
        self.job_id = None

    def run(self, **kwargs) -> None:
        """Run the job management

        :param kwargs: The keyword arguments to pass to the launch_job_template method

        :rtype: None
        :return: Runs the inventory builder
        """
        self.job_template_id = self.get_job_template_id(name=self.job_template_name)
        self.inventory_id = self.get_inventory_id(name=self.inventory_name)
        self.job_id = self.launch_job_template(
            job_template_id=self.job_template_id, inventory=self.inventory_id, **kwargs
        ).get("id")

    def poll_completion(self, print_status: Optional[bool] = False, **kwargs) -> str:  # pragma: no cover
        """Run the job and poll the completion of a job

        :type print_status: Optional[bool] = False
        :param print_status: Print the status of the job

        :param kwargs: The keyword arguments to pass to the launch_job_template method

        :rtype: String
        :returns: The completed status of the job

        :raises TypeError: If print_status is not of type bool
        """
        if not isinstance(print_status, bool):
            raise TypeError(f"print_status must be of type bool, but received {type(print_status)}")

        if not self.job_id:
            self.run(**kwargs)

        ok_statuses = ["successful", "failed", "error", "cancelled"]

        job_status = "new"

        if print_status:
            print(f"Polling job_id {self.job_id} current status {job_status}")

        while job_status not in ok_statuses:
            time.sleep(5)
            job_status = self.get_job_status(job_id=self.job_id)

            if print_status:
                print(f"Polling job_id {self.job_id} current status {job_status}")

            if job_status in ok_statuses:
                break

        if print_status:
            print(f"Polling job_id {self.job_id} completed status {job_status}")

        return job_status

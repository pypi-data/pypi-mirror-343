"""
AAP Jobs
"""

from typing import Optional, Literal
from ansible_aap_api_client.base_connection import _BaseConnection


class Job(_BaseConnection):
    """Job class

    :type base_url: str
    :param base_url: The base url to use
    :type username: str
    :param username: The username to use
    :type password: str
    :param password: The password to use
    :type ssl_verify: Optional[Union[bool, str]] = True
    :param ssl_verify: The SSL verification True or False or a path to a certificate
    """

    jobs_uri = "/jobs/"

    def get_all_jobs(self) -> dict:
        """Get all jobs

        :rtype: Dict
        :returns: Response
        """
        return self._get(uri=self.jobs_uri).json()

    def get_job(self, job_id: int) -> dict:
        """Get a job by id

        :type job_id: int
        :param job_id: The ID of the job

        :rtype: Dict
        :returns: Response

        :raises TypeError: If name is not of type str
        """
        uri = f"{self.jobs_uri}{job_id}/"
        if not isinstance(job_id, int):
            raise TypeError(f"job_id must be of type int, but received {type(job_id)}")

        return self._get(uri=uri).json()

    def get_job_stdout(self, job_id: int, output_format: Optional[Literal["txt", "json", "html"]] = "txt") -> str:
        """Get the stdout of a job by id, this is the ansible run log

        :type job_id: int
        :param job_id: The ID of the job
        :type output_format: Optional[Literal["txt", "json", "html"]] = "txt"
        :param output_format: The format of the output

        :rtype: str
        :returns: The stdout of the job

        :raises TypeError: If name is not of type str
        """
        uri = f"{self.jobs_uri}{job_id}/stdout/"

        if not isinstance(job_id, int):
            raise TypeError(f"job_id must be of type int, but received {type(job_id)}")

        return self._get(uri=uri, params={"format": output_format}).text

    def get_job_status(self, job_id: int) -> str:
        """Get the status of a job by id

        :type job_id: int
        :param job_id: The ID of the job

        :rtype: str
        :returns: The status of the job

        :raises TypeError: If name is not of type str
        """
        if not isinstance(job_id, int):
            raise TypeError(f"job_id must be of type int, but received {type(job_id)}")

        return self.get_job(job_id=job_id).get("status")

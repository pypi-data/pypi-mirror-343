"""
AAP API client for job templates
"""

from ansible_aap_api_client.base_connection import _BaseConnection


class JobTemplate(_BaseConnection):
    """Job Templates class

    :type base_url: str
    :param base_url: The base url to use
    :type username: str
    :param username: The username to use
    :type password: str
    :param password: The password to use
    :type ssl_verify: Optional[Union[bool, str]] = True
    :param ssl_verify: The SSL verification True or False or a path to a certificate
    """

    job_templates_uri = "/job_templates/"

    def get_all_job_templates(self) -> dict:
        """Get all job templates

        :rtype: Dict
        :returns: Response
        """
        return self._get(uri=self.job_templates_uri).json()

    def get_job_template(self, name: str) -> dict:
        """Get all instances of a job template by name

        :type name: str
        :param name: The name of the job template

        :rtype: Dict
        :returns: Response

        :raises TypeError: If name is not of type str
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be of type str, but received {type(name)}")

        return self._get(uri=self.job_templates_uri, params={"name": name}).json()

    def get_job_template_id(self, name: str) -> int:
        """Get the id of a job template if one exists

        :type name: str
        :param name: The name of the job template

        :rtype: int
        :returns: The id of the job template

        :raises ValueError: If zero or more than one instance is found
        :raises TypeError: If name is not of type str
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be of type str, but received {type(name)}")

        response = self.get_job_template(name=name).get("results")
        if len(response) != 1:
            raise ValueError(f"Expected 1 job template, but received {len(response)}")

        return response[0]["id"]

    def launch_job_template(self, job_template_id: int, **kwargs) -> dict:
        """Launch a job template

        :type job_template_id: int
        :param job_template_id: The id of the job template

        :param kwargs: The key word args to launch the job with, example: inventory=1, extra_vars={"key": "value"}

        :rtype: Dict
        :returns: Response

        :raises TypeError: If job_template_id is not of type int
        """
        uri = f"{self.job_templates_uri}{job_template_id}/launch/"

        if not isinstance(job_template_id, int):
            raise TypeError(f"job_template_id must be of type int, but received {type(job_template_id)}")

        return self._post(uri=uri, json_data=kwargs).json()

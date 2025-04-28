"""
AAP Groups
"""

from ansible_aap_api_client.base_connection import _BaseConnection
from ansible_aap_api_client.schemas import InventoryHostRequestSchema


class Host(_BaseConnection):
    """Host class

    :type base_url: str
    :param base_url: The base url to use
    :type username: str
    :param username: The username to use
    :type password: str
    :param password: The password to use
    :type ssl_verify: Optional[Union[bool, str]] = True
    :param ssl_verify: The SSL verification True or False or a path to a certificate
    """

    hosts_uri = "/hosts/"

    def get_all_hosts(self) -> dict:
        """Get all hosts

        :rtype: Dict
        :returns: Response
        """
        return self._get(uri=self.hosts_uri).json()

    def get_host(self, name: str) -> dict:
        """Get all instances of a host by name

        :type name: str
        :param name: The name of the host

        :rtype: Dict
        :returns: Response

        :raises TypeError: If name is not of type str
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be of type str, but received {type(name)}")

        return self._get(uri=self.hosts_uri, params={"name": name}).json()

    def get_host_id(self, name: str) -> int:
        """Get the id of a host if one exists

        :type name: str
        :param name: The name of the host

        :rtype: int
        :returns: The id of the host

        :raises ValueError: If zero or more than one instance is found
        :raises TypeError: If name is not of type str
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be of type str, but received {type(name)}")

        response = self.get_host(name=name).get("results")

        if len(response) != 1:
            raise ValueError(f"Expected 1 result, but received {len(response)}")

        return response[0]["id"]

    def delete_host(self, host_id: int) -> int:
        """Delete a host

        :type host_id: int
        :param host_id: The id of the host

        :rtype: int
        :returns: The id of the deleted host
        """
        uri = f"{self.hosts_uri}{host_id}/"

        if not isinstance(host_id, int):
            raise TypeError(f"host_id must be of type int, but received {type(host_id)}")

        return self._delete(uri=uri).status_code

    def update_host(self, host_id: int, host: InventoryHostRequestSchema) -> dict:
        """Update a host

        :type host_id: int
        :param host_id: The id of the host
        :type host: InventoryHostRequestSchema
        :param host: The host object

        :rtype: dict
        :returns: The updated host
        """
        uri = f"{self.hosts_uri}{host_id}/"

        if not isinstance(host_id, int):
            raise TypeError(f"host_id must be of type int, but received {type(host_id)}")

        if not isinstance(host, InventoryHostRequestSchema):
            raise TypeError(f"host must be of type InventoryHostRequestSchema, but received {type(host)}")

        return self._patch(uri=uri, json_data=host.dict()).json()

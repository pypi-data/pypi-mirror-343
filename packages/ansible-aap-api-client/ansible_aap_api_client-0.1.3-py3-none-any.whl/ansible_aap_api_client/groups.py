"""
AAP Groups
"""

from ansible_aap_api_client.base_connection import _BaseConnection
from ansible_aap_api_client.schemas import InventoryHostRequestSchema, InventoryGroupRequestSchema


class Group(_BaseConnection):
    """Group class

    :type base_url: str
    :param base_url: The base url to use
    :type username: str
    :param username: The username to use
    :type password: str
    :param password: The password to use
    :type ssl_verify: Optional[Union[bool, str]] = True
    :param ssl_verify: The SSL verification True or False or a path to a certificate
    """

    groups_uri = "/groups/"

    def get_all_groups(self) -> dict:
        """Get all groups

        :rtype: Dict
        :returns: Response
        """
        return self._get(uri=self.groups_uri).json()

    def get_group(self, name: str) -> dict:
        """Get all instances of a group by name

        :type name: str
        :param name: The name of the group

        :rtype: Dict
        :returns: Response

        :raises TypeError: If name is not of type str
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be of type str, but received {type(name)}")

        return self._get(uri=self.groups_uri, params={"name": name}).json()

    def get_group_id(self, name: str) -> int:
        """Get the id of a group if one exists

        :type name: str
        :param name: The name of the group

        :rtype: int
        :returns: The id of the group

        :raises ValueError: If zero or more than one instance is found
        :raises TypeError: If name is not of type str
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be of type str, but received {type(name)}")

        response = self.get_group(name=name).get("results")

        if len(response) != 1:
            raise ValueError(f"found {len(response)} groups with name {name}")

        return response[0]["id"]

    def delete_group(self, group_id: int) -> int:
        """Delete group

        :type group_id: int
        :param group_id: The group id

        :rtype: Integer
        :returns: Response Status Code

        :raises TypeError: If inventory_id is not of type int
        """
        uri = f"{self.groups_uri}{group_id}/"

        if not isinstance(group_id, int):
            raise TypeError(f"group_id must be of type int, but received {type(group_id)}")

        return self._delete(uri=uri).status_code

    def update_group(self, group_id: int, group: InventoryGroupRequestSchema) -> dict:
        """Update group

        :type group_id: int
        :param group_id: The group id
        :type group: InventoryGroupRequestSchema
        :param group: The group data

        :rtype: Dict
        :returns: Response

        :raises TypeError: If inventory is not a InventoryRequestSchema
        :raises TypeError: If inventory_id is not of type int
        """
        uri = f"{self.groups_uri}{group_id}/"

        if not isinstance(group_id, int):
            raise TypeError(f"group_id must be of type int, but received {type(group_id)}")

        if not isinstance(group, InventoryGroupRequestSchema):
            raise TypeError(f"group must be of type InventoryGroupRequestSchema, but received {type(group)}")

        return self._patch(uri=uri, json_data=group.dict()).json()

    def add_host_to_group(self, group_id: int, host: InventoryHostRequestSchema) -> dict:
        """Add host to group

        :type group_id: int
        :param group_id: The group id
        :type host: InventoryHostRequestSchema
        :param host: The host to add

        :rtype: Dict
        :returns: Response

        :raises TypeError: If host is not of type InventoryHostRequestSchema
        """
        uri = f"{self.groups_uri}{group_id}/hosts/"

        if not isinstance(group_id, int):
            raise TypeError(f"group_id must be of type int, but received {type(group_id)}")

        if not isinstance(host, InventoryHostRequestSchema):
            raise TypeError(f"host must be of type InventoryHostRequestSchema, but received {type(host)}")

        return self._post(uri=uri, json_data=host.dict()).json()

"""
AAP API client for inventory management
"""

from typing import List, Union
from ansible_aap_api_client.inventories import Inventory
from ansible_aap_api_client.schemas import (
    InventoryRequestSchema,
    InventoryGroupRequestSchema,
    InventoryHostRequestSchema,
)
from ansible_aap_api_client.hosts import Host
from ansible_aap_api_client.groups import Group
from ansible_aap_api_client.interfaces.runable import Runable


class InventoryManagement(Inventory, Group, Host):
    """Inventory management class

    :type base_url: str
    :param base_url: The base url to use
    :type username: str
    :param username: The username to use
    :type password: str
    :param password: The password to use
    :type ssl_verify: Optional[Union[bool, str]] = True
    :param ssl_verify: The SSL verification True or False or a path to a certificate
    """


class InventoryBuilder(Runable, InventoryManagement):  # pylint: disable=too-many-instance-attributes
    """Inventory builder class, this builds an inventory with groups and hosts

    :type base_url: str
    :param base_url: The base url to use
    :type username: str
    :param username: The username to use
    :type password: str
    :param password: The password to use
    :type ssl_verify: Union[bool, str]
    :param ssl_verify: The SSL verification True or False or a path to a certificate

    :raises TypeError: If inventory is not an instance of InventoryRequestSchema
    """

    IOS_GROUP_VARS = {
        "ansible_connection": "ansible.netcommon.network_cli",
        "ansible_become": True,
        "ansible_become_method": "enable",
        "ansible_network_os": "ios",
    }

    IOSXR_GROUP_VARS = {
        "ansible_connection": "ansible.netcommon.network_cli",
        "ansible_become": True,
        "ansible_become_method": "enable",
        "ansible_network_os": "iosxr",
    }

    NXOS_GROUP_VARS = {
        "ansible_connection": "ansible.netcommon.network_cli",
        "ansible_become": True,
        "ansible_become_method": "enable",
        "ansible_network_os": "nxos",
    }

    EOS_GROUP_VARS = {
        "ansible_connection": "ansible.netcommon.network_cli",
        "ansible_become": True,
        "ansible_become_method": "enable",
        "ansible_network_os": "eos",
    }

    def __init__(  # pylint: disable=too-many-arguments
        self,
        base_url: str,
        username: str,
        password: str,
        ssl_verify: Union[bool, str],
        inventory: InventoryRequestSchema,
    ) -> None:
        super().__init__(base_url, username, password, ssl_verify)

        if not isinstance(inventory, InventoryRequestSchema):
            raise TypeError(f"inventory must be an instance of InventoryRequestSchema but received a {type(inventory)}")

        self.inventory = inventory
        self.inventory_name = inventory.name
        self.inventory_id = None

        self.ios_group_id = None
        self.ios_hosts = []

        self.iosxr_group_id = None
        self.iosxr_hosts = []

        self.nxos_group_id = None
        self.nxos_hosts = []

        self.eos_group_id = None
        self.eos_hosts = []

        self.custom_groups = []
        self.custom_groups_data = {}
        self.custom_hosts = []

    def run(self) -> None:
        """Run the inventory builder

        :rtype: None
        :return: Runs the inventory builder
        """
        self.inventory_id = self.create_inventory(inventory=self.inventory).get("id")

        self.ios_group_id = self.add_group_to_inventory(
            inventory_id=self.inventory_id,
            group=self._get_group_request_schema("ios"),
        ).get("id")

        for host in self.ios_hosts:
            self.add_host_to_group(group_id=self.ios_group_id, host=host)

        self.iosxr_group_id = self.add_group_to_inventory(
            inventory_id=self.inventory_id,
            group=self._get_group_request_schema("iosxr"),
        ).get("id")

        for host in self.iosxr_hosts:
            self.add_host_to_group(group_id=self.iosxr_group_id, host=host)

        self.nxos_group_id = self.add_group_to_inventory(
            inventory_id=self.inventory_id,
            group=self._get_group_request_schema("nxos"),
        ).get("id")

        for host in self.nxos_hosts:
            self.add_host_to_group(group_id=self.nxos_group_id, host=host)

        self.eos_group_id = self.add_group_to_inventory(
            inventory_id=self.inventory_id,
            group=self._get_group_request_schema("eos"),
        ).get("id")

        for host in self.eos_hosts:
            self.add_host_to_group(group_id=self.eos_group_id, host=host)

        for group in self.custom_groups:
            response = self.add_group_to_inventory(inventory_id=self.inventory_id, group=group)
            self.custom_groups_data[group.name] = response.get("id")

        for host in self.custom_hosts:
            self.add_host_to_group(group_id=self.custom_groups_data[host["group_name"]], host=host["host"])

    def _get_group_request_schema(self, nos: str) -> InventoryGroupRequestSchema:
        """Protected method to get group request schema

        :type nos: str
        :param nos: The NOS to use

        :rtype: InventoryGroupRequestSchema
        :return: The group request schema

        :raises ValueError: If the NOS is not supported
        """
        if nos == "ios":
            group_vars = self.IOS_GROUP_VARS
        elif nos == "iosxr":
            group_vars = self.IOSXR_GROUP_VARS
        elif nos == "nxos":
            group_vars = self.NXOS_GROUP_VARS
        elif nos == "eos":
            group_vars = self.EOS_GROUP_VARS
        else:
            raise ValueError(f"Unsupported NOS: {nos}")

        return InventoryGroupRequestSchema(
            name=f"{self.inventory_name}-{nos}",
            description=f"Inventory {self.inventory_name} Group for {nos} devices",
            variables=group_vars,
        )

    def add_ios_host_to_inventory(self, host: InventoryHostRequestSchema) -> None:
        """Add IOS host to inventory

        :type host: InventoryHostRequestSchema
        :param host: The host to add

        :rtype: None
        :return: Adds the host to the inventory

        :raises TypeError: If host is not an instance of InventoryHostRequestSchema
        """
        if not isinstance(host, InventoryHostRequestSchema):
            raise TypeError(f"host must be an instance of InventoryHostRequestSchema but received a {type(host)}")

        self.ios_hosts.append(host)

    def add_ios_hosts_to_inventory(self, hosts: List[InventoryHostRequestSchema]) -> None:
        """Add multiple IOS hosts to inventory

        :type hosts: List[InventoryHostRequestSchema]
        :param hosts: The hosts to add

        :rtype: None
        :return: Adds the hosts to the inventory

        :raises TypeError: If hosts is not a list of InventoryHostRequestSchema
        """
        if not all(isinstance(host, InventoryHostRequestSchema) for host in hosts):
            raise TypeError(f"hosts must be a list of InventoryHostRequestSchema but received a list of {type(hosts)}")

        self.ios_hosts.extend(hosts)

    def add_iosxr_host_to_inventory(self, host: InventoryHostRequestSchema) -> None:
        """Add IOS-XR host to inventory

        :type host: InventoryHostRequestSchema
        :param host: The host to add

        :rtype: None
        :return: Adds the host to the inventory

        :raises TypeError: If host is not an instance of InventoryHostRequestSchema
        """
        if not isinstance(host, InventoryHostRequestSchema):
            raise TypeError(f"host must be an instance of InventoryHostRequestSchema but received a {type(host)}")

        self.iosxr_hosts.append(host)

    def add_iosxr_hosts_to_inventory(self, hosts: List[InventoryHostRequestSchema]) -> None:
        """Add multiple IOS-XR hosts to inventory

        :type hosts: List[InventoryHostRequestSchema]
        :param hosts: The hosts to add

        :rtype: None
        :return: Adds the hosts to the inventory

        :raises TypeError: If hosts is not a list of InventoryHostRequestSchema
        """
        if not all(isinstance(host, InventoryHostRequestSchema) for host in hosts):
            raise TypeError(f"hosts must be a list of InventoryHostRequestSchema but received a list of {type(hosts)}")

        self.iosxr_hosts.extend(hosts)

    def add_nxos_host_to_inventory(self, host: InventoryHostRequestSchema) -> None:
        """Add NX-OS host to inventory

        :type host: InventoryHostRequestSchema
        :param host: The host to add

        :rtype: None
        :return: Adds the host to the inventory

        :raises TypeError: If host is not an instance of InventoryHostRequestSchema
        """
        if not isinstance(host, InventoryHostRequestSchema):
            raise TypeError(f"host must be an instance of InventoryHostRequestSchema but received a {type(host)}")

        self.nxos_hosts.append(host)

    def add_nxos_hosts_to_inventory(self, hosts: List[InventoryHostRequestSchema]) -> None:
        """Add multiple NX-OS hosts to inventory

        :type hosts: List[InventoryHostRequestSchema]
        :param hosts: The hosts to add

        :rtype: None
        :return: Adds the hosts to the inventory

        :raises TypeError: If hosts is not a list of InventoryHostRequestSchema
        """
        if not all(isinstance(host, InventoryHostRequestSchema) for host in hosts):
            raise TypeError(f"hosts must be a list of InventoryHostRequestSchema but received a list of {type(hosts)}")

        self.nxos_hosts.extend(hosts)

    def add_eos_host_to_inventory(self, host: InventoryHostRequestSchema) -> None:
        """Add EOS host to inventory

        :type host: InventoryHostRequestSchema
        :param host: The host to add

        :rtype: None
        :return: Adds the host to the inventory

        :raises TypeError: If host is not an instance of InventoryHostRequestSchema
        """
        if not isinstance(host, InventoryHostRequestSchema):
            raise TypeError(f"host must be an instance of InventoryHostRequestSchema but received a {type(host)}")

        self.eos_hosts.append(host)

    def add_eos_hosts_to_inventory(self, hosts: List[InventoryHostRequestSchema]) -> None:
        """Add multiple EOS hosts to inventory

        :type hosts: List[InventoryHostRequestSchema]
        :param hosts: The hosts to add

        :rtype: None
        :return: Adds the hosts to the inventory

        :raises TypeError: If hosts is not a list of InventoryHostRequestSchema
        """
        if not all(isinstance(host, InventoryHostRequestSchema) for host in hosts):
            raise TypeError(f"hosts must be a list of InventoryHostRequestSchema but received a list of {type(hosts)}")

        self.eos_hosts.extend(hosts)

    def add_custom_group_to_inventory(self, group: InventoryGroupRequestSchema) -> None:
        """Add custom group to inventory

        :type group: InventoryGroupRequestSchema
        :param group: The group to add

        :rtype: None
        :return: Adds the custom group to the inventory

        :raises TypeError: If group is not an instance of InventoryGroupRequestSchema
        """
        if not isinstance(group, InventoryGroupRequestSchema):
            raise TypeError(f"group must be an instance of InventoryGroupRequestSchema but received a {type(group)}")

        self.custom_groups.append(group)

    def add_custom_groups_to_inventory(self, groups: List[InventoryGroupRequestSchema]) -> None:
        """Add custom group to inventory

        :type groups: List[InventoryGroupRequestSchema]
        :param groups: The groups to add

        :rtype: None
        :return: Adds the custom groups to the inventory

        :raises TypeError: If groups is not a list of InventoryGroupRequestSchema
        """
        if not all(isinstance(group, InventoryGroupRequestSchema) for group in groups):
            raise TypeError(
                f"groups must be a list of InventoryGroupRequestSchema but received a list of {type(groups)}"
            )

        self.custom_groups.extend(groups)

    def add_host_to_custom_group_to_inventory(self, group_name: str, host: InventoryHostRequestSchema) -> None:
        """Add host to custom group to inventory

        :type group_name: str
        :param group_name: The group name to add the host to
        :type host: InventoryHostRequestSchema
        :param host: The host to add

        :rtype: None
        :return: Adds the host to the inventory

        :raises TypeError: If group_name is not a string or host is not an instance of InventoryHostRequestSchema
        """
        if not isinstance(group_name, str):
            raise TypeError(f"group_name must be a string but received a {type(group_name)}")

        if not isinstance(host, InventoryHostRequestSchema):
            raise TypeError(f"host must be an instance of InventoryHostRequestSchema but received a {type(host)}")

        self.custom_hosts.append({"group_name": group_name, "host": host})

    def add_hosts_to_custom_group_to_inventory(self, group_name: str, hosts: List[InventoryHostRequestSchema]) -> None:
        """Add hosts to custom group to inventory

        :type group_name: str
        :param group_name: The group name to add the hosts to
        :type hosts: List[InventoryHostRequestSchema]
        :param hosts: The hosts to add

        :rtype: None
        :return: Adds the hosts to the inventory

        :raises TypeError: If group_name is not a string or hosts is not a list of InventoryHostRequestSchema
        """
        if not isinstance(group_name, str):
            raise TypeError(f"group_name must be a string but received a {type(group_name)}")

        if not all(isinstance(host, InventoryHostRequestSchema) for host in hosts):
            raise TypeError(f"hosts must be a list of InventoryHostRequestSchema but received a list of {type(hosts)}")

        for host in hosts:
            self.custom_hosts.append({"group_name": group_name, "host": host})

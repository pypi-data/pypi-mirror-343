"""
AAP API client for organizations
"""

from ansible_aap_api_client.base_connection import _BaseConnection
from ansible_aap_api_client.schemas import OrganizationRequestSchema


class Organization(_BaseConnection):
    """Organization class

    :type base_url: str
    :param base_url: The base url to use
    :type username: str
    :param username: The username to use
    :type password: str
    :param password: The password to use
    :type ssl_verify: Optional[Union[bool, str]] = True
    :param ssl_verify: The SSL verification True or False or a path to a certificate
    """

    organizations_uri = "/organizations/"

    def get_all_organizations(self) -> dict:
        """Get all organizations

        :rtype: Dict
        :returns: Response
        """
        return self._get(uri=self.organizations_uri).json()

    def get_organization(self, name: str) -> dict:
        """Get all instances of an organization by name

        :type name: str
        :param name: The name of the organization

        :rtype: Dict
        :returns: Response

        :raises TypeError: If name is not of type str
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be of type str, but received {type(name)}")

        return self._get(uri=self.organizations_uri, params={"name": name}).json()

    def get_organization_id(self, name: str) -> int:
        """Get the id of an organization if one exists

        :type name: str
        :param name: The name of the organization

        :rtype: int
        :returns: The id of the organization

        :raises ValueError: If zero or more than one instance is found
        :raises TypeError: If name is not of type str
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be of type str, but received {type(name)}")

        response = self.get_organization(name=name).get("results")

        if len(response) != 1:
            raise ValueError(f"found {len(response)} organizations with name {name}")

        return response[0]["id"]

    def delete_organization(self, organization_id: int) -> int:
        """Delete organization

        :type organization_id: int
        :param organization_id: The id of the organization

        :rtype: Integer
        :returns: Response Status Code

        :raises TypeError: If organization_id is not of type int
        """
        uri = f"{self.organizations_uri}{organization_id}/"

        if not isinstance(organization_id, int):
            raise TypeError(f"organization_id must be of type int, but received {type(organization_id)}")

        return self._delete(uri=uri).status_code

    def update_organization(self, organization_id: int, organization: OrganizationRequestSchema) -> dict:
        """Update a organization

        :type organization_id: int
        :param organization_id: The id of the OrganizationRequestSchema
        :type organization: InventoryHostRequestSchema
        :param organization: The organization object

        :rtype: dict
        :returns: The updated host

        :raises TypeError: If organization_id is not of type int
        :raises TypeError: If organization is not of type OrganizationRequestSchema
        """
        uri = f"{self.organizations_uri}{organization_id}/"

        if not isinstance(organization_id, int):
            raise TypeError(f"organization_id must be of type int, but received {type(organization_id)}")

        if not isinstance(organization, OrganizationRequestSchema):
            raise TypeError(
                f"organization must be of type OrganizationRequestSchema, but received {type(organization)}"
            )

        return self._patch(uri=uri, json_data=organization.dict()).json()

    def create_organization(self, organization: OrganizationRequestSchema):
        """Create an organization

        :type organization: OrganizationRequestSchema
        :param organization: The organization object

        :rtype: dict
        :returns: The created organization

        :raises TypeError: If organization is not of type OrganizationRequestSchema
        """
        if not isinstance(organization, OrganizationRequestSchema):
            raise TypeError(
                f"organization must be of type OrganizationRequestSchema, but received {type(organization)}"
            )

        return self._post(uri=self.organizations_uri, json_data=organization.dict()).json()

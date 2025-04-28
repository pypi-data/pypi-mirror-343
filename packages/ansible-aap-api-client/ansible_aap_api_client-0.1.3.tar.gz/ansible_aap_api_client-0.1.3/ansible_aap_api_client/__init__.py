"""
init for ansible_aap_api_client
"""

from ansible_aap_api_client.ansible_aap_api_client_cli import cli
from ansible_aap_api_client.inventories import Inventory
from ansible_aap_api_client.groups import Group
from ansible_aap_api_client.hosts import Host
from ansible_aap_api_client.organizations import Organization
from ansible_aap_api_client.job_templates import JobTemplate
from ansible_aap_api_client.jobs import Job
from ansible_aap_api_client.inventory_management import InventoryManagement, InventoryBuilder
from ansible_aap_api_client.job_management import JobManagement
from ansible_aap_api_client.schemas import (
    InventoryRequestSchema,
    InventoryHostRequestSchema,
    InventoryGroupRequestSchema,
    OrganizationRequestSchema,
)

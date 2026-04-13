# """
# TECOMTP Manager Module

# Provides management functionality for the ECOM module.
# """

# from .entrypoint import ecom_manager

# __all__ = ["ecom_manager"]


from fluvius.fastapi import (
    create_app,
    configure_authentication,
    configure_domain_manager,
    configure_query_manager)

from fluvius.navis.domain import WorkflowDomain, WorkflowQueryManager
from fluvius.fastapi.auth_mock import FluviusMockProfileProvider
from fluvius.mcp import configure_mcp_server
# from fluvius_beam import configure_beam_client
# Import the loan application process workflow
# from . import process
from ecom_domain import ecom_client


domains = (
    'ecom_domain.ecom_client.ECOMClientServiceDomain',
    # WorkflowDomain,
    # 'rfx_idm.IDMDomain',
    # 'rfx_user.UserProfileDomain',
    # 'rfx_message.RFXMessageServiceDomain',
    # 'kitchen_task.KitchenTaskDomain',
    # 'fluvius_beam.FluviusBeamDomain',
)

queries = (
    'ecom_domain.ecom_client.ECOMClientQueryManager',
    # WorkflowQueryManager,
    # 'rfx_idm.IDMQueryManager',
    # 'rfx_user.UserProfileQueryManager',
    # 'rfx_message.RFXMessageServiceQueryManager',
    # 'kitchen_task.KitchenTaskQueryManager',
    # 'fluvius_beam.FluviusBeamQueryManager',
)

app = create_app(root_path='/api/v1') \
    | configure_authentication(auth_profile_provider=FluviusMockProfileProvider) \
    | configure_domain_manager(*domains) \
    | configure_query_manager(*queries) \
    | configure_mcp_server()

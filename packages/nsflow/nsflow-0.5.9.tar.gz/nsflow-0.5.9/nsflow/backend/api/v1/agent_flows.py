
# Copyright (C) 2023-2025 Cognizant Digital Business, Evolutionary AI.
# All Rights Reserved.
# Issued under the Academic Public License.
#
# You can be released from the terms, and requirements of the Academic Public
# License by purchasing a commercial license.
# Purchase of a commercial license is mandatory for any use of the
# nsflow SDK Software in commercial settings.
#
# END COPYRIGHT
# nsflow/backend/api/v1/agent_flows.py

import logging
from fastapi import APIRouter
from nsflow.backend.utils.agent_network_utils import AgentNetworkUtils

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/api/v1")
agent_utils = AgentNetworkUtils()  # Instantiate utility class


@router.get("/networks/")
def get_networks():
    """Returns a list of available agent networks."""
    return agent_utils.list_available_networks()


@router.get("/network/{network_name}", responses={200: {"description": "Agent Network found"},
                                                  404: {"description": "Agent Network not found"}})
def get_agent_network(network_name: str):
    """Retrieves the network structure for a given agent network."""
    file_path = agent_utils.get_network_file_path(network_name)
    logging.info("file_path: %s", file_path)
    return agent_utils.parse_agent_network(file_path)


@router.get("/connectivity/{network_name}", responses={200: {"description": "Connectivity Info"},
                                                       404: {"description": "HOCON file not found"}})
def get_connectivity_info(network_name: str):
    """Retrieves connectivity details from a HOCON network configuration file."""
    file_path = agent_utils.get_network_file_path(network_name)
    logging.info("file_path: %s", file_path)
    return agent_utils.extract_connectivity_info(file_path)


@router.get("/networkconfig/{network_name}", responses={200: {"description": "Connectivity Info"},
                                                        404: {"description": "HOCON file not found"}})
def get_networkconfig(network_name: str):
    """Retrieves the entire details from a HOCON network configuration file."""
    file_path = agent_utils.get_network_file_path(network_name)
    logging.info("file_path: %s", file_path)
    return agent_utils.load_hocon_config(file_path)


@router.get("/networkconfig/{network_name}/agent/{agent_name}", responses={200: {"description": "Agent Info found"},
                                                                           404: {"description": "Info not found"}})
def fetch_agent_info(network_name: str, agent_name: str):
    """Retrieves the entire details of an Agent from a HOCON network configuration file."""
    file_path = agent_utils.get_network_file_path(network_name)
    logging.info("file_path: %s, agent_name: %s", file_path, agent_name)
    return agent_utils.get_agent_details(file_path, agent_name)

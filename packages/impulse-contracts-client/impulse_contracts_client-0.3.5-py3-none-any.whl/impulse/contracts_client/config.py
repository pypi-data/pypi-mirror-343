import os
from typing import Tuple

import click
from dotenv import load_dotenv
from eth_typing import HexStr
from impulse.contracts_client.client import ImpulseConfig, load_contract_artifacts
from impulse.contracts_client.constants import (
    ENV_VAR_RPC_URL,
    ENV_VAR_USER_PRIVATE_KEY,
    ENV_VAR_NODE_PRIVATE_KEY,
    DEFAULT_RPC_URL, DEFAULT_IMPULSE_DIR
)
from impulse.contracts_client.utils import read_env_vars


def load_environment() -> None:
    """Load environment variables from .env files"""
    # Load local env vars
    load_dotenv('./.env', override=True)

    # Load user env vars
    load_dotenv(os.path.expanduser(f'{DEFAULT_IMPULSE_DIR}/.env'), override=True)


def setup_environment_vars(is_node: bool = False) -> Tuple[str, str]:
    """Set up environment variables, prompting for missing values
    
    Args:
        is_node: True if setting up for node client, False for user client
        
    Returns:
        Tuple of (rpc_url, private_key)
    """
    # Set up the ~/.impulse directory if it doesn't exist
    impulse_dir = os.path.expanduser(DEFAULT_IMPULSE_DIR)
    os.makedirs(impulse_dir, exist_ok=True)
    env_file = os.path.join(impulse_dir, '.env')

    # Get the appropriate private key env var name
    private_key_var = ENV_VAR_NODE_PRIVATE_KEY if is_node else ENV_VAR_USER_PRIVATE_KEY

    # Check if we need to prompt for missing credentials
    rpc_url = os.getenv(ENV_VAR_RPC_URL)
    private_key = os.getenv(private_key_var)

    if not rpc_url or not private_key:
        # Read ALL existing env vars if file exists to preserve them
        existing_env = read_env_vars(env_file, {
            ENV_VAR_RPC_URL: 'RPC URL',
            private_key_var: 'Private Key'
        })

        print("Impulse client setup required")

        # Get RPC URL if needed
        if not rpc_url:
            rpc_url = click.prompt(
                "Enter RPC URL for blockchain connection",
                default=DEFAULT_RPC_URL
            )
            existing_env[ENV_VAR_RPC_URL] = rpc_url
            os.environ[ENV_VAR_RPC_URL] = rpc_url

        # Get private key if needed
        if not private_key:
            private_key = click.prompt(
                f"Enter {'node' if is_node else 'your'} private key (will be stored securely)",
                hide_input=True
            )
            # Ensure it's in the correct format (with 0x prefix)
            if not private_key.startswith('0x'):
                private_key = '0x' + private_key
            existing_env[private_key_var] = private_key
            os.environ[private_key_var] = private_key

        # Save updated env vars, preserving all existing ones
        with open(env_file, 'w') as f:
            for key, value in existing_env.items():
                f.write(f"{key}={value}\n")

        # Reload environment
        load_dotenv(env_file, override=True)

    return rpc_url, private_key


def create_sdk_config(is_node: bool = False) -> ImpulseConfig:
    """Create SDK configuration
    
    Args:
        is_node: True if creating for node client, False for user client
        
    Returns:
        ImpulseConfig instance
    """
    # Get contracts and ABIs
    contracts_addresses, abis_dir = load_contract_artifacts()

    # Get private key var based on client type
    private_key_var = ENV_VAR_NODE_PRIVATE_KEY if is_node else ENV_VAR_USER_PRIVATE_KEY

    # Create SDK config
    return ImpulseConfig(
        web3_provider=os.getenv(ENV_VAR_RPC_URL, DEFAULT_RPC_URL),
        contract_addresses=contracts_addresses,
        abis_dir=abis_dir,
        private_key=HexStr(os.getenv(private_key_var)),
    )

# Impulse Contracts Client

A Python client for interacting with the Impulse protocol, a decentralized computing platform for machine learning jobs.

## Overview

The Impulse Contracts Client provides two main executables:

- `impulse-node`: For node operators to participate in the Impulse network
- `impulse-client`: For users to submit and monitor jobs on the network

## Installation

### Requirements

- Python 3.12
- An Ethereum wallet address
- Impulse tokens
- ETH for gas fees
- RPC endpoint for the blockchain
- `python` command available in your PATH and pointing to Python 3.12 (`python --version` should return `3.12.x`)
- `pip` command available in your PATH and pointing to Python 3.12 (`pip --version` should point to `python 3.12`)

### Installing via pip

```bash
pip install impulse-contracts-client
export PATH=$HOME/.local/bin:$PATH  # Add Python bin to PATH
```

## Configuration

Both clients create a `$HOME/.impulse` directory for storing state:

- Node artifacts and configuration
- Client state and job information
- Logs and temporary files

## Node Client (`impulse-node`)

### Features

- Interacts with smart contracts for leader election, job assignment, and incentives
- Executes machine learning jobs upon assignment
- Automatically manages node's stake on the node escrow (i.e. top-up)
- Registers node to the Impulse network

### Requirements

- A whitelisted Ethereum address
- Impulse tokens transferred to the address
- The impulse artifacts password
- Some ETH for gas costs
- Compatible GPU hardware

### Supported GPU Hardware

- 1, 2, 4, or 8x NVIDIA A100 (40GB or 80GB)
- 8x NVIDIA H100 (80GB)

### Running the Node

```bash
impulse-node
```

## User Client (`impulse-client`)

### Features

- Submits machine learning jobs to the Impulse network
- Monitors job execution and retrieves results
- Manages user's balance on the job escrow contract

### Basic Usage

Top up your balance for paying for jobs:

```bash
impulse-client topup
```

### Submitting Jobs

Example dummy job:

```bash
impulse-client create-job --args '{"shuffle": true, "use_lora": true, "use_qlora": false, "batch_size": 4, "dataset_id": "gs://imp-dev-pipeline-zen-datasets/0ca98b07-9366-4a31-8c83-569961c90294/2024-12-17_21-57-21_text2sql.jsonl", "num_epochs": 1, "job_config_name": "llm_dummy"}' --model llm_dummy --ft_type "LORA" --monitor
```

Example LLaMA 3.2 1B LoRA job:

```bash
impulse-client create-job --args '{"shuffle": true, "use_lora": true, "use_qlora": false, "batch_size": 4, "dataset_id": "gs://imp-dev-pipeline-zen-datasets/0ca98b07-9366-4a31-8c83-569961c90294/2024-12-17_21-57-21_text2sql.jsonl", "num_epochs": 1, "job_config_name": "llm_llama3_2_1b"}' --model llm_llama3_2_1b --ft_type "LORA"
```

### Monitoring Jobs

Monitor all submitted jobs:

```bash
impulse-client monitor-all
```

## Development

For development setup and contributing guidelines, see [DEVEL.md](DEVEL.md).
from setuptools import setup

# Read README.md file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from VERSION file
with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

# Read requirements from requirements.txt file
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="impulse-contracts-client",
    version=version,
    author="Impulse Labs AI",
    author_email="engg@impulselabs.ai",
    license="MIT",
    description="Client for interacting with the Impulse Labs protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/impulselabs/contracts-client",
    package_dir={"": "src"},
    python_requires=">=3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "impulse-node = impulse.contracts_client.node_client:main",
            "impulse-client = impulse.contracts_client.user_client:cli",
        ],
    },
)

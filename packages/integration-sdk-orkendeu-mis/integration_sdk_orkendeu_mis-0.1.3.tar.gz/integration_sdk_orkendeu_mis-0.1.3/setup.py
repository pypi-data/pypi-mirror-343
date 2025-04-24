from setuptools import setup, find_packages

setup(
    name="integration_sdk_orkendeu_mis",
    version="0.1.3",
    packages=find_packages(where="."),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "pydantic",
        "httpx",
        "lxml",
        "tenacity",
        "redis",
        "uvicorn",
        "pytest",
        "aioredis"
    ],
)
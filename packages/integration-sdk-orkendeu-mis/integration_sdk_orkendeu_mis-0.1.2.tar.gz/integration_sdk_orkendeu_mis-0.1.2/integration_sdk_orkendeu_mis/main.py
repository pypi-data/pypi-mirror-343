from fastapi import FastAPI

from src.mock_integration.api import endpoints

app = FastAPI(
    title="Integration SDK",
    description="Integration SDK for handling various integration requests",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "integration_sdk_orkendeu_mis",
            "description": "Integration SDK endpoints"
        }
    ]
)

app.include_router(endpoints.router, prefix="/api/v1", tags=["integration_sdk_orkendeu_mis"])
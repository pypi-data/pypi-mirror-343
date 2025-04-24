from fastapi import APIRouter, HTTPException

from src.mock_integration.api.schemas.request.base_integration_request import BaseIntegrationRequest
from src.mock_integration.api.schemas.response.base_integration_response import BaseIntegrationResponse
from integration_sdk_orkendeu_mis.handlers.dto.handler_result_dto import HandlerResultDTO
from src.mock_integration.handlers.get_person_info_handler import GetPersonInfoMockHandler

router = APIRouter()


@router.post("/get-person-info", response_model=BaseIntegrationResponse)
async def get_person_info(request: BaseIntegrationRequest):
    handler = GetPersonInfoMockHandler()
    result: HandlerResultDTO = await handler.handle(request.payload.dict())

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    return BaseIntegrationResponse(success=True, data=result.data)
from datetime import datetime

from pydantic import BaseModel

from elluminate.schemas.base import BatchCreateStatus
from elluminate.schemas.generation_metadata import GenerationMetadata
from elluminate.schemas.prompt import Prompt
from elluminate.schemas.rating import Rating


class PromptResponse(BaseModel):
    """Prompt response model."""

    id: int
    prompt: Prompt
    response: str
    generation_metadata: GenerationMetadata | None
    epoch: int
    ratings: list[Rating] = []
    created_at: datetime


class CreatePromptResponseRequest(BaseModel):
    """Request to create a new prompt response."""

    prompt_template_id: int
    template_variables_id: int
    llm_config_id: int | None = None
    response: str | None = None
    metadata: GenerationMetadata | None = None


class BatchCreatePromptResponseRequest(BaseModel):
    prompt_response_ins: list[CreatePromptResponseRequest]


class BatchCreatePromptResponseStatus(BatchCreateStatus[PromptResponse]):
    # The result is a tuple with epoch and response
    pass

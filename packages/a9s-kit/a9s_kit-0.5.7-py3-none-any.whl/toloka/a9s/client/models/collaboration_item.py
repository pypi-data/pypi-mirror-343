from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DocumentBytes(BaseModel):
    type: Literal['Buffer']
    data: list[int]


class CollaborationItemResponse(BaseModel):
    id: str
    document: DocumentBytes
    json_data: dict[str, Any] = Field(..., alias='json')
    createdAt: str
    updatedAt: str
    version: int

    model_config = ConfigDict(populate_by_name=True)


class CollaborationItemPatch(BaseModel):
    field: str
    value: Any

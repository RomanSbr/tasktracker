from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)
    sort_by: Optional[str] = "created_at"
    sort_order: str = Field("desc", pattern="^(asc|desc)$")


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: List[T]
    page: int
    per_page: int
    total: int
    total_pages: int

    class Config:
        from_attributes = True


class ResponseModel(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    errors: Optional[List[str]] = None

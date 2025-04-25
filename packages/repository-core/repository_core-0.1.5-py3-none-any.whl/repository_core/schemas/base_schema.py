from datetime import datetime
from typing import Any, List, Optional, Literal, Union, Dict
from uuid import UUID

from pydantic import BaseModel, Field

from ..utils import make_optional

class ModelBaseInfo(BaseModel):
    id: int
    uuid: UUID
    created_at: datetime
    updated_at: datetime



# Primitive field condition
class FieldOperatorCondition(BaseModel):
    field: str
    operator: Literal["eq", "neq", "gt", "gte", "lt", "lte", "in", "not_in", "like", "ilike", "between", "is_null", "is_not_null"]
    value: Any

# Base structure for a logical group
class LogicalCondition(BaseModel):
    operator: Literal["AND", "OR"]
    conditions: List["ConditionType"]


# Each item in conditions list can be:
# 1. a logical condition (nested group)
# 2. a dict like {field: ..., operator: ..., value: ...}
ConditionType = Union["LogicalCondition", "FieldOperatorCondition"]



# Top-level filter schema
class FilterSchema(BaseModel):
    operator: Literal["AND", "OR"]
    conditions: List[ConditionType]

class SortOrder(BaseModel):
    field: str
    direction: Literal["asc", "desc"]

class FindBase(BaseModel):
    sort_orders: Optional[List[SortOrder]] = None
    page: Optional[int] = 1
    page_size: Optional[int] = 10
    search: Optional[str] = None
    filters: Optional[FilterSchema] = None



class SearchOptions(FindBase):
    total_count: Optional[int] = None


class FindResult(BaseModel):
    founds: Optional[List] = None
    search_options: Optional[SearchOptions] = None

class FindUniqueValues(BaseModel):
    field_name: str
    ordering: Optional[Literal["asc", "desc"]]=None
    page: Optional[int]=1
    page_size: Optional[int]=10
    search: Optional[str]=None


class UniqueValuesResult(BaseModel):
    founds: List[Any]
    search_options: Optional[SearchOptions] = None

from enum import Enum
from pydantic import BaseModel
from typing import Optional, List

class FieldTypeEnum(str, Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    STRING = "string"
    LIST = "list"
    MAP = "map"

class Field(BaseModel):
    name: str
    type: FieldTypeEnum
    description: Optional[str] = None


class TypeDef(BaseModel):
    name: str
    description: Optional[str] = None
    fields: List[Field]

class Spec(BaseModel):
    types: List[TypeDef]

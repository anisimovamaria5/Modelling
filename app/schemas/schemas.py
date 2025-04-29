from pydantic import BaseModel
from typing import List, Literal

class DataPoint(BaseModel):
    x: float
    y: float

class Dataset(BaseModel):
    label: Literal['polytropic efficiency', 'head coefficient']
    title: str 
    kind:  Literal['points', 'line']
    data: List[DataPoint]

class CurveResponse(BaseModel):
    datasets: List[Dataset]
    label: str

class ComapaniesPydantic(BaseModel):
    id: int
    label: str

class FieldPydantic(BaseModel):
    id: int
    label: str  
    companies_id: List[ComapaniesPydantic]

class DksPydantic(BaseModel):
    id: int
    label: str
    field_id: List[FieldPydantic]

class FilterItem(BaseModel):
    id: int
    label: str
    code: str
    chidren: List["FilterItem"] | None





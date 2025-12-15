from pydantic import BaseModel, field_serializer, field_validator
from typing import List, Literal, Optional


class DataPoint(BaseModel):
    """
    Координаты для построения графика 
    
    """
    x: float
    y: float


class Dataset(BaseModel):
    """
    Схема датасета со значениями безразмерных параметров для кпд и коэффициента напора для графиков (линии и точки)
    
    """
    label: Literal['polytropic efficiency', 'head coefficient']
    title: str 
    kind:  Literal['points', 'line']
    data: List[DataPoint]


class CurveResponse(BaseModel):
    """
    Схема датасета с названиями СПЧ
    
    """
    datasets: List[Dataset]
    label: str


class FilterItem(BaseModel):
    """
    Схема для формирования json для моделей: недропользователь, месторождение и ДКС
    
    """
    id: int
    name: str
    code: str


class SubMenu(BaseModel):
    """
    Схема для формирования json вложенного меню

    """
    name: str
    code: str
    children: Optional[List["SubMenu"]] | None


class DataBuild(BaseModel):
    """
    Координаты для построения графика 

    """
    label: str
    data: List[DataPoint]
    kind: Optional[Literal["kpd" , "freq"]] = None


class GdhDetail(BaseModel):
    """
    Схема датасета с координатами для построения ГДХ

    """
    SPCHName: str
    paramline: str    
    datasets: List[DataBuild]


class ShortName(BaseModel):
    """
    Схема имени СПЧ по номиналам

    """
    comp_nom: float
    power_nom: int
    p_out_nom: int


class GdhList(BaseModel):
    """
    Схема СПЧ 

    """
    id: int
    name: str
    dks_name: str
    dks_code: str
    field_name: str
    company_name: str
    shortName: ShortName

    @field_serializer("shortName")
    def validate_short_name(self, v: ShortName) -> str:
        return  f'{v.power_nom:.0f}-{v.p_out_nom:.0f} {v.comp_nom}'


class StageType(GdhList):
    """
    Схема СПЧ с параметрами и количеством агрегатов

    """
    count_GPA: int


class Conf(BaseModel):
    """
    Схема компановки 

    """   
    stage_list:List[StageType]


class BoundName(BaseModel):
    """
    Схема имен параметров граничных условий

    """
    name: str
    short_name: str
    dimen: str | None
    disable: bool = False


class BoundParamValue(BoundName):
    """
    Схема значений параметров

    """
    value: float


class BoundParam(BoundName):
    """
    Схема мин/макс значений граничных условий

    """
    min_value: float
    max_value: float
    sensitivity: float
    precision: int    


class BoundDict(BaseModel):
    """
    Схема значений граничных условий

    """
    p_out_diff: BoundParam
    freq_dimm: BoundParam
    power: BoundParam
    comp: BoundParam
    udal: BoundParam

class BoundExtraParam(BaseModel):
    """
    Схема экстра параметров

    """
    k_value: BoundParamValue
    t_in: BoundParamValue
    r_value: BoundParamValue  
    press_conditonal: BoundParamValue 
    temp_conditonal: BoundParamValue


class BoundDictAll(BaseModel):
    """
    Схема значений граничных условий с экстра параметрами

    """
    bounds: BoundDict
    extra_bounds: BoundExtraParam


class ModeParam(BaseModel):
    """
    Схема задаваемых параметров без экстра параметров

    """
    q_rate: List[float] | float
    p_in: float
    p_target: float

    @field_validator('p_in', 'p_target', mode='before')
    def convert_list_to_float(cls, v):
        if isinstance(v, list):
            return v[0]
        return v
    

class TableParam(BaseModel):
    """
    Схема задаваемых параметров без экстра параметров

    """
    q_rate: List[float]
    p_out: List[float]


class ModeParamAll(ModeParam):
    """
    Схема задаваемых параметров с экстра параметрами 

    """
    t_in: float
    r_value: float
    k_value: float
    press_conditonal: float 
    temp_conditonal: float



class Calc(ModeParam):
    """
    Полная схема режимов работы 
    
    """
    p_in_result: List[float]
    p_out: List[float]
    freq: List[int]
    title: List[str]
    power: List[float]
    comp: List[float]
    work_gpa: List[int]
    target: List[float]
    udal: List[float]
    volume_rate: List[float]


"""Модуль с эндпойтами-обработчиками запросов от клиентов"""
from typing import Literal, List
from fastapi import APIRouter, Depends, Query, UploadFile, File
from app_name.infrastructure.repositories.base_repository import BaseRepository
from app_name.application.compressor_unit_service import CompressorUnitServise
from app_name.application.menu_service import _build_tree
from app_name.UI.api.dependencies import *
from app_name.UI.api.middlewares import handle_errors
from app_name.infrastructure.repositories.compressor.models.models_gdh  import *
from app_name.UI.api.schemas.schemas import *


router = APIRouter(prefix='/api/v1')

@router.post("/upload/{filetype}/preview/",
            response_model = List[CurveResponse] | None,
            operation_id = "upload",
            name = "upload"
            )
@handle_errors
async def upload_excel_file(
    filetype: Literal['normal','flowrate'],
    deg: int = 4,
    k_value: float = 1.31,
    press_conditional: float = 0.101325,
    temp_conditional: float = 283,
    file: UploadFile = File(...),
    serv: CompressorUnitServise = Depends(get_unit_service)
    ):
    """Эндпойнт формирования базы ГДХ\n
    \tРасчитываются безразмерные парметры (коэффициент расхода, коэффициент напора и кпд) для построения безразмерных ГДХ"""
    dct_df = await serv.get_df_by_xlsx(file,
                                    deg=deg,
                                    k_value=k_value,
                                    press_conditional=press_conditional,
                                    temp_conditional=temp_conditional
                                    )
    return await serv.get_param(dct_df)


@router.post("/save/{filetype}/commit/",
            operation_id = "save",
            name = "save"
            )
@handle_errors
async def save_excel_file(
    filetype: Literal['normal','flowrate'],
    sheet_name:str,
    dks_code:str,
    deg: int = 4,
    k_value: float = 1.31,
    press_conditonal: float = 0.101325,
    temp_conditonal: float = 283,
    file: UploadFile = File(...),
    serv: CompressorUnitServise = Depends(get_unit_service)
    ):
    """Эндпойнт сохранения ГДХ в БД\n"""

    dct_df = await serv.get_df_by_xlsx(file,
                                    deg=deg,
                                    k_value=k_value,
                                    press_conditonal=press_conditonal,
                                    temp_conditonal=temp_conditonal
                                    )
    return await serv.create_unit(dct_df, 
                                  sheet_name, 
                                  dks_code)


@router.post("/calc/",
            response_model = List[Calc],
            name="calc",
            operation_id = "calc",
            )
@handle_errors
async def get_calc(
    conf_gdh: List[Conf],
    mode: List[ModeParamAll],
    bound_dict: List[List[BoundDictAll]],
    deg: int = Query(4, gt=0),
    serv: CompressorUnitServise = Depends(get_unit_service)
    ):
    """Эндпойнт получения таблицы с итоговыми режимами\n"""

    lst_param_all_gdh = []
    for conf in conf_gdh:
        lst = [await serv.get_gdh_by_unit_id(stage.id) for stage in conf.stage_list]
        lst_param_all_gdh.append(lst)
    return await serv.calc_of_modes(
        lst_param_all_gdh,
        [[stage.count_GPA for stage in conf.stage_list] for conf in conf_gdh],
        mode,
        bound_dict,
        deg
    )


@router.post("/calc_vfp/",
            # response_model = List[Calc],
            name="calc_vfp",
            operation_id = "calc_vfp",
            )
@handle_errors
async def get_calc_vfp(
    conf_gdh: List[Conf],
    table_params: TableParam,
    bound_dict: List[List[BoundDictAll]],
    deg: int = Query(4, gt=0),
    serv: CompressorUnitServise = Depends(get_unit_service)
    ):
    """Эндпойнт получения таблицы vfp\n"""
    
    lst_param_all_gdh = []
    for conf in conf_gdh:
        lst = [await serv.get_gdh_by_unit_id(stage.id) for stage in conf.stage_list]
        lst_param_all_gdh.append(lst)
    return await serv.calc_vfp(
        lst_param_all_gdh,
        [[stage.count_GPA for stage in conf.stage_list] for conf in conf_gdh],
        table_params,
        bound_dict,
        deg
    )


@router.delete("/delete/",
            name="delete"
            )
@handle_errors
async def delete_data(
    repo: BaseRepository = Depends(get_model_repo(Dks))
    ):
    """Эндпойнт удаления\n"""

    return await repo.delete_data_all(hard=True)


@router.get("/company/",
            response_model = List[FilterItem],
            operation_id = "company",
            name="company"
            )
@handle_errors
async def get_all_companies(
    repo: BaseRepository = Depends(get_model_repo(Company))
    ):
    """Эндпойнт получения списка всех компаний из базы данных\n"""

    return await repo.get_data()


@router.get("/company/{company_code}/field/",
            response_model = List[FilterItem],
            operation_id = "field",
            name="field"
            )
@handle_errors
async def get_all_field(
    company_code: str,
    repo: BaseRepository = Depends(get_model_repo(Field))
    ):
    """Эндпойнт получения списка месторождений по company_code недропользователя из базы данных\n"""

    return await repo.get_data_by_code(company_code)
    

@router.get("/company/field/{field_code}/dks/",
            response_model = List[FilterItem],
            operation_id = "dks",
            name="dks"
            )
@handle_errors
async def get_all_dks(
    field_code: str,
    repo: BaseRepository = Depends(get_model_repo(Dks))
    ):
    """Эндпойнт получения списка ДКС по field_code месторождения из базы данных\n"""

    return await repo.get_data_by_code(field_code)


@router.get("/gdh/",
            response_model = List[GdhList],
            operation_id = "gdh_list",
            name="gdh_list"
            )
@handle_errors
async def get_spch(
    repo: CompressorUnitServise = Depends(get_unit_service)
    ):
    """Эндпойнт получения списка СПЧ из базы данных\n"""

    return await repo.read_data()


@router.get("/company_tree/",
            response_model = List[SubMenu],
            operation_id = "company_tree",
            name="company_tree"
            )
@handle_errors
async def get_bread_crumbs(
    repo: BaseRepository = Depends(get_model_repo(Company))
    ):
    """Эндпойнт получения вложенного меню\n"""

    return await _build_tree(repo)


@router.get("/gdh/{id}/",
            response_model = GdhDetail,
            operation_id = "gdh_detail",
            name="gdh_detail"
            )
@handle_errors
async def get_gdh_by_id(
    id: int,
    serv: CompressorUnitServise = Depends(get_unit_service)
    ):
    """Эндпойнт построения ГДХ\n"""

    result = await serv.get_gdh_by_unit_id(id)
    return await serv.get_param_for_gdh(result)


@router.get("/default_bound/",
            response_model = BoundDictAll,
            operation_id = "default_bound",
            name="default_bound"
            )
@handle_errors
async def get_default_values(
    serv: CompressorUnitServise = Depends(get_unit_service)
    ):
    """Эндпойнт получения дефолтных значений\n"""

    extra_bounds = await serv.get_extra_param()
    bounds = await serv.read_data_uom()
    return {
        'bounds': bounds,
        'extra_bounds': extra_bounds
    }



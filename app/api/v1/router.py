"""Модуль с эндпойтами-обработчиками запросов от клиентов"""
import logging
from typing import Literal, List
from fastapi import APIRouter, Depends, Query, UploadFile, File
from app.repositories.base_repository import BaseRepository
from app.repositories.compressor.unit_repository import CompressorUnitRepository
from app.services.compressor_unit_service import CompressorUnitServise
from app.services.menu_service import _build_tree
from app.dependencies import get_db_session, get_model_repo, get_unit_repo, get_unit_service
from app.middlewares import handle_errors
from app.models.models_gdh  import UOM, Dimension, Dks, EqCompressorPerfomanceCurve, Company, Field
from app.schemas.schemas import *
from io import BytesIO



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
    press_conditonal: float = 0.101325,
    temp_conditonal: float = 283,
    file: UploadFile = File(...),
    serv: CompressorUnitServise = Depends(get_unit_service)
    ):
    """
    Эндпойнт формирования базы ГДХ\n
    \tРасчитываются безразмерные парметры 
    (коэффициент расхода, коэффициент напора и кпд) для построения безразмерных ГДХ.
    
    """
    dct_df = await serv.get_df_by_xls(file,
                                    deg=deg,
                                    k_value=k_value,
                                    press_conditonal=press_conditonal,
                                    temp_conditonal=temp_conditonal
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
    """
    Эндпойнт сохранения ГДХ в БД\n

    """
    dct_df = await serv.get_df_by_xls(file,
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
    conf_gdh: Conf,
    mode: List[ModeParamAll],
    bound_dict: List[BoundDictAll],
    deg: int = Query(4, gt=0),
    serv: CompressorUnitServise = Depends(get_unit_service)
    ):
    """
    Эндпойнт получения таблицы для расчетов\n

    """
    return [{
            "q_rate": [
                35.0,
                35.0
            ],
            "p_in": 3.0,
            "p_target": 7.0,
            "p_in_result": [
                3.0,
                4.239999834224764
            ],
            "p_out": [
                4.299999834224764,
                7.000000009226201
            ],
            "freq": [
                3591,
                3977
            ],
            "title": [
                "НЦ 16-41 2.2",
                "нц 16-76 2.2"
            ],
            "power": [
                9674.02555438503,
                9219.21166284354
            ],
            "comp": [
                1.4333332780749213,
                1.6509434629508828
            ],
            "work_gpa": [
                2,
                3
            ],
            "target": [
                2.7000001657752364,
                9.226201136414147e-09
            ],
            "udal": [
                71.26513229809864,
                58.61895525136729
            ],
            "volume_rate": [
                393.475116387859,
                180.6994313213335
            ]
            }] * len(mode)
    # return await serv.calc_of_modes(
    #     [await serv.get_gdh_by_unit_id(stage.id) for stage in conf_gdh.stage_list],
    #     [stage.count_GPA for stage in conf_gdh.stage_list],
    #     mode,
    #     bound_dict,
    #     deg
    # )


@router.delete("/delete/",
            name="delete"
            )
@handle_errors
async def delete_data(
    repo: BaseRepository = Depends(get_model_repo(UOM))
    ):
    """
    Эндпойнт удаления\n

    """
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
    """
    Эндпойнт получения списка всех компаний из базы данных\n

    """
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
    """
    Эндпойнт получения списка месторождений по id недропользователя из базы данных\n

    """
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
    """
    Эндпойнт получения списка ДКС по id месторождения из базы данных\n

    """
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
    """
    Эндпойнт получения списка СПЧ из базы данных\n

    """
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
    """
    Эндпойнт получения вложенного меню\n

    """
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
    """
    Эндпойнт построения ГДХ\n

    """
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
    """
    Эндпойнт получения дефолтных значений\n

    """
    extra_bounds = await serv.get_extra_param()
    bounds = await serv.read_data_uom()
    return {
        'bounds': bounds,
        'extra_bounds': extra_bounds
    }



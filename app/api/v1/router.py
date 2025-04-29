"""Модуль с эндпойтами-обработчиками запросов от клиентов"""
import logging
import os
from typing import Literal, Optional, List
from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
import pandas as pd
from DKS_math.shared import get_df_by_excel, use_pydantic_model
from app.schemas.schemas import *
from io import BytesIO

router = APIRouter(prefix='/api/v1')  # роутер, объединяющий эндпойнты API с единым префиксом
datafile_logger = logging.getLogger('datafile')  # ссылаемся на логгер парсера


@router.post("/upload/{filetype}/{kind}",
            response_model = List[CurveResponse] | None,
            operation_id = "upload",
            name = "upload"
            )
async def upload_excel_file(
    kind: Literal['preview','commit'],
    filetype: Literal['normal','flowrate'],
    deg: int = 4,
    k_value: float = 1.31,
    press_conditonal: float = 0.101325,
    temp_conditonal: float = 283,
    file: UploadFile = File(...),
    ):
    if kind == 'commit':
        pass
    elif kind == 'preview':
        file_content = await file.read()
        excel_data = BytesIO(file_content)
        lst_df = get_df_by_excel(
            excel_data,
            deg=deg,
            k_value=k_value,
            press_conditonal=press_conditonal,
            temp_conditonal=temp_conditonal
            )
        curves = use_pydantic_model(lst_df)
        return curves

@router.get("/companies",
            # response_model = List[CurveResponse] | None,
            operation_id="companies",
            name="companies"
            )
async def get_all_companies():pass


@router.post("/companies",
             response_model = List[FilterItem],
             name = "companies")
async def create_company():


@router.post("/fields",
             response_model = List[FilterItem],
             name = "fields")
async def create_field():
    

@router.post("/dks",
             response_model = List[FilterItem],
             name = "dks")
async def create_dks():
    
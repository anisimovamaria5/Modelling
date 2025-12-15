from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import Query
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app_name.UI.cli.default_setting_service import DefaultSettingService
from app_name.application.menu_service import _build_tree
from app_name.infrastructure.repositories.base_repository import BaseRepository
from app_name.infrastructure.repositories.compressor.models.models_gdh import Company, Dks, Field
from app_name.application.compressor_unit_service import CompressorUnitServise
from app_name.UI.api.schemas.schemas import Conf, ModeParamAll, BoundDictAll, TableParam


class CLIService:
    """Сервисный слой для CLI команд"""

    def __init__(self, 
                 session: AsyncSession,
                 ):
        self.session = session
        self.compressor_service = CompressorUnitServise(session)
        self.default_setting_service = DefaultSettingService(Path())


    def _get_repo(self, model) -> BaseRepository:
        """Создание экземпляра репозитория"""
        return BaseRepository(self.session, model)
        

    async def upload_excel(self,
            file: Path,
            deg: int = None,
            k_value: float = None,
            press_conditional: float = None,
            temp_conditional: float = None,
        ):

        """Загрузка безразмерных ГДХ"""

        dct_df = await self.compressor_service.get_df_by_xlsx(
                                            file,
                                            deg,
                                            k_value,
                                            press_conditional,
                                            temp_conditional)
        results = await self.compressor_service.get_param(dct_df)
        return results


    async def save_to_db(self,
            sheet_name: str,
            dks_code: str,
            file: Path,
            deg: int = None,
            k_value: float = None,
            press_conditional: float = None,
            temp_conditional: float = None,
        ):

        """Сохранения СПЧ в базу данных"""

        dct_df = await self.compressor_service.get_df_by_xlsx(
                                                file,
                                                deg,
                                                k_value,
                                                press_conditional,
                                                temp_conditional)
        results = await self.compressor_service.create_unit(dct_df, 
                                  sheet_name, 
                                  dks_code)
        return results
    

    async def calculate_modes(self,
            conf_gdh: List[Conf],
            mode: List[ModeParamAll],
            bound_dict: List[List[BoundDictAll]],
            deg: int = None
        ) -> List[pd.DataFrame]:
        
        """Расчет прогнозных режимов ДКС"""

        lst_param_all_gdh = []
        for conf in conf_gdh:
            lst = [await self.compressor_service.get_gdh_by_unit_id(stage.id) for stage in conf.stage_list]
            lst_param_all_gdh.append(lst)

        result = await self.compressor_service.calc_of_modes(
            lst_param_all_gdh,
            [[stage.count_GPA for stage in conf.stage_list] for conf in conf_gdh],
            mode,
            bound_dict,
            deg
        )
        return result


    async def calculate_vfp(self,
            conf_gdh: List[Conf],
            table_params: TableParam,
            bound_dict: List[List[BoundDictAll]],
            deg: int = None
        ) -> List[pd.DataFrame]:
        
        """Расчет таблицы VFP"""

        lst_param_all_gdh = []
        for conf in conf_gdh:
            lst = [await self.compressor_service.get_gdh_by_unit_id(stage.id) for stage in conf.stage_list]
            lst_param_all_gdh.append(lst)

        result = await self.compressor_service.calc_vfp(
            lst_param_all_gdh,
            [[stage.count_GPA for stage in conf.stage_list] for conf in conf_gdh],
            table_params,
            bound_dict,
            deg
        )
        return result
    
    
    async def get_gdh_by_id(self, id:int) -> Dict:

        """Получение размерных ГДХ"""

        result = await self.compressor_service.get_gdh_by_unit_id(id)
        return await self.compressor_service.get_param_for_gdh(result)
    

    async def get_list_spch(self) -> List[Dict]:

        """Получение списка СПЧ из базы данных"""

        result = await self.compressor_service.read_data()
        return result
    

    async def get_bread_crumbs(self) -> List[Dict]:

        """Получение вложенного меню"""

        repo = self._get_repo(Company)
        result = await _build_tree(repo)
        return result
    





    async def get_all_companies(self) -> List[Dict]:

        """Получение списка всех компаний из базы данных"""

        repo = self._get_repo(Company)
        result = await repo.get_data()
        return result
    
    async def get_list_fields(self, company_code:str) -> List[Dict]:

        """Получение списка месторождений по company_code недропользователя из базы данных"""

        repo = self._get_repo(Field)
        result = await repo.get_data_by_code(company_code)
        return result

    async def get_list_dks(self, field_code:str) -> List[Dict]:

        """Получение списка ДКС по field_code месторождения из базы данных"""

        repo = self._get_repo(Dks)
        result = await repo.get_data_by_code(field_code)
        return result
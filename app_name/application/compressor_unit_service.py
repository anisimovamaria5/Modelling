from sqlalchemy.ext.asyncio import AsyncSession
from app_name.UI.api.schemas.schemas import *
from app_name.infrastructure.repositories.compressor.unit_repository import CompressorUnitRepository
from io import BytesIO
from app_name.DKS_math.shared.shared_gdh import BaseGDH, get_df_by_excel, get_param
from app_name.DKS_math.shared.shared_calc import calc_vfp, calc_of_modes


class CompressorUnitServise(CompressorUnitRepository):
    def __init__(self, session: AsyncSession):
        self.repository = CompressorUnitRepository(session)


    async def get_gdh_by_unit_id(self, id: int):
        result = await self.repository.read_data_by_id(id)
        return result
    

    async def get_param_for_gdh(self, result):
        param = BaseGDH.read_dict(result[0]) 
        res = param.get_param()    
        return res        

    
    async def read_data(self):
        result = await self.repository.read_data()
        return result    


    async def get_df_by_xlsx(self, 
                            file,
                            deg,
                            k_value,
                            press_conditonal,
                            temp_conditonal):
        file_content = await file.read()
        excel_data = BytesIO(file_content)
        dct_df = get_df_by_excel(
                        excel_data,
                        deg=deg,
                        k_value=k_value,
                        press_conditonal=press_conditonal,
                        temp_conditonal=temp_conditonal
                        )
        return dct_df
    

    async def create_unit(self, dct_df, sheet_name, dks_code):
        df = dct_df[sheet_name]
        perfomance_curves = [
                            {
                            'k_nap' : df['k_nap'][i],
                            'k_rash' : df['k_rash'][i],
                            'kpd' : df['kpd'][i],
                            }
                            for i in range(len(df['k_nap']))
                            ]
        return await self.repository.create_compressor_unit(
                        sheet_name=sheet_name,
                        dks_code=dks_code,
                        pressure_out=df['p_title'][0],
                        comp_ratio=df['stepen'][0],
                        freq_nominal=df['fnom'][0],
                        power=df['mgth'][0],
                        k_value=df['k'][0],
                        r_value=df['R'][0],
                        t_in=df['temp'][0],
                        diam=df['diam'][0],
                        perfomance_curves=perfomance_curves
                    )


    async def get_param(self, dct_df):
        curves = get_param(dct_df)
        return curves
    

    async def get_extra_param(self):
        result = await self.repository.uom_repo.get_data()
        output = {}
        all_param = [
                'k_value',                
                't_in', 
                'r_value', 
                'press_conditonal', 
                'temp_conditonal'
                ]
        values = {
            'k_value': {"value": 1.31},
            't_in': {"value": 288},
            'r_value': {"value": 512},  
            'press_conditonal': {"value": 0.101325},
            'temp_conditonal': {"value": 283},
        }
        for param in all_param:
            item = next((x for x in result if x.uom_code == param), None)
            dimen = await self.repository.read_data_by_id_uom(item.dimen_id)
            if item is not None:
                output[param] = {
                        "name": item.name,
                        "short_name": item.short_name,
                        "dimen": dimen,
                        "disable": False,
                        "value": values[param]['value']
                    }
        return output
    

    async def read_data_uom(self):
        result = await self.repository.uom_repo.get_data()
        output = {}
        all_param = [
                'p_out_diff',
                'freq_dimm',                
                'power', 
                'comp', 
                'udal', 
                ]
        
        for param in all_param:
            item = next((x for x in result if x.uom_code == param), None)
            dimen = await self.repository.read_data_by_id_uom(item.dimen_id)
            if item is not None:
                output[param] = {
                        "name": item.name,
                        "short_name": item.short_name,
                        "dimen": dimen,
                        "disable": False,
                        "min_value": DefaultBoundValues.get_defaults(param)['min_value'],
                        "max_value": DefaultBoundValues.get_defaults(param)['max_value'],
                        "sensitivity": DefaultBoundValues.get_defaults(param)['sensitivity'],
                        "precision": DefaultBoundValues.get_defaults(param)['precision']
                        } 
        return output
    

    async def calc_of_modes(self, 
                            lst_params,
                            lst_cnt,
                            mode,
                            bound_dict,
                            deg):
        result = await calc_of_modes(
                            lst_params,
                            lst_cnt,
                            mode,
                            bound_dict,
                            deg
                            )
        return [res.to_dict('list') for res in result]

    

    async def calc_vfp(self, 
                        lst_params,
                        lst_cnt,
                        table_params,
                        bound_dict,
                        deg):
        result = await calc_vfp(
                            lst_params,
                            lst_cnt,
                            table_params,
                            bound_dict,
                            deg
                            )
        return result
    

class DefaultBoundValues:
    DEFAULT = { 
        "p_out_diff": 
            {
            "min_value": 0.1,
            "max_value": 7.7,
            "sensitivity": 0.1,
            "precision": 0
            },
        "freq_dimm": 
            {
            "min_value": 0.7,
            "max_value": 1.05,
            "sensitivity": 0.1,
            "precision": 2
            },
        "power": 
            {
            "min_value":7000,
            "max_value": 16000,
            "sensitivity": 200,
            "precision": 0
            },
        "comp": 
            {
            "min_value": 1,
            "max_value": 3.5,
            "sensitivity": 0.01,
            "precision": 2
            },
        "udal": 
            {
            "min_value": 0,
            "max_value": 100,
            "sensitivity": 1,
            "precision": 0
            }
            }
    

    @classmethod
    def get_defaults(cls, param_name):
        return cls.DEFAULT.get(param_name,
                            {
                            "min_value": 0,
                            "max_value": 0,
                            "sensitivity": 0,
                            "precision": 0
                        })
    

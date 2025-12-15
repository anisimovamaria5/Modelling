from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app_name.infrastructure.repositories.compressor.models.models_gdh import *
from sqlalchemy.orm import selectinload

from app_name.infrastructure.repositories.base_repository import BaseRepository

class CompressorUnitRepository(BaseRepository[EqCompressorUnit]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, EqCompressorUnit)
        self.uom_repo = BaseRepository(session, UOM)


    async def read_data_by_id(self, id):
        result = await self.session.execute(
            select(EqCompressorUnit)
            .options(selectinload(EqCompressorUnit.eq_compressor_perfomance_curve),
                     selectinload(EqCompressorUnit.eq_compressor_type)
                     .selectinload(EqCompressorType.eq_compressor_type_freq_nominal),
                     selectinload(EqCompressorUnit.eq_compressor_type)
                     .selectinload(EqCompressorType.eq_compressor_type_comp_ratio),
                     selectinload(EqCompressorUnit.eq_compressor_type)
                     .selectinload(EqCompressorType.eq_compressor_type_pressure_out),
                     selectinload(EqCompressorUnit.eq_compressor_type)
                     .selectinload(EqCompressorType.eq_compressor_type_power)
                     )
            .where(EqCompressorUnit.id == id)
        )
        return result.scalars().all()
    

    async def read_data_by_id_uom(self, id):
        result = await self.session.execute(
            select(Dimension.dimen)
            .join(UOM.dimen)
            .where(UOM.dimen_id == id)
            .limit(1)
        )
        return result.scalar_one()
    

    async def read_data(self):
        result = await self.session.execute(
            select(
                EqCompressorUnit.id,
                EqCompressorUnit.name,
                Dks.name.label("dks_name"),
                Dks.code.label("dks_code"),
                Field.name.label("field_name"),
                Company.name.label("company_name"),
                EqCompressorTypePressureOut.value.label("p_out_nom"),
                EqCompressorTypeCompRatio.value.label("comp_nom"),
                EqCompressorTypePower.value.label("power_nom")
                )
                .join(EqCompressorUnit.dks)
                .join(Dks.field)
                .join(Field.company)             
                .join(EqCompressorUnit.eq_compressor_type)
                .join(EqCompressorType.eq_compressor_type_pressure_out)
                .join(EqCompressorType.eq_compressor_type_comp_ratio)
                .join(EqCompressorType.eq_compressor_type_power)
                    )
        data = result.mappings().all()

        return [{
                "id": item['id'],
                "name": item['name'],
                "dks_name": item['dks_name'],
                "dks_code": item['dks_code'],
                "field_name": item['field_name'],
                "company_name": item['company_name'],
                "shortName":{
                    "p_out_nom": item['p_out_nom'],
                    "comp_nom": item['comp_nom'],
                    "power_nom": item['power_nom']                
                    }
                } 
                for item in data]


    async def create_compressor_unit(self,
                        sheet_name: str,
                        dks_code: str,
                        pressure_out: float,
                        comp_ratio: float,
                        freq_nominal: float,
                        power: float,
                        k_value: float,
                        r_value: float,
                        t_in: float,
                        diam: float,
                        perfomance_curves: list[dict]
                    ):
        dks_id = await self.session.scalar(
                                    select(Dks.id)
                                    .where(Dks.code == dks_code)
                                    )    
          
        type_params = [
                    (EqCompressorTypePressureOut, pressure_out, 'press_out_id'),
                    (EqCompressorTypeCompRatio, comp_ratio, 'comp_ratio_id'),
                    (EqCompressorTypeFreqNomimal, freq_nominal, 'freq_nominal_id'),
                    (EqCompressorTypePower, power, 'power_id')
                    ]
        dct_result_id = {}     
        for model, param, id_param in type_params:
            repo_param = BaseRepository(self.session, model)
            type_param = await repo_param.create_if_not_exist(value=param)
            dct_result_id[id_param] = type_param

        repo_compressor = BaseRepository(self.session, EqCompressorType)
        compressor_type = await repo_compressor.create_if_not_exist(**dct_result_id)

        unit = EqCompressorUnit(
                            name=sheet_name,
                            dks_id=dks_id,
                            type_id=compressor_type,
                            k_value=k_value, 
                            r_value=r_value,
                            t_in=t_in,
                            diam=diam
                            )
        self.session.add(unit)
        await self.session.flush()


        for curve in perfomance_curves:
            perf_curve = EqCompressorPerfomanceCurve(
                            unit_id=unit.id,
                            head=curve['k_nap'],
                            non_dim_rate=curve['k_rash'],
                            kpd=curve['kpd'],
                            )
            self.session.add(perf_curve)
        
        await self.session.commit()
        return unit
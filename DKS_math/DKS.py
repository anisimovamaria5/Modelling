import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from itertools import product
import cProfile
import asyncio
import copy
import time
from  datetime import datetime as dt
from concurrent.futures import ProcessPoolExecutor
from DKS_math.logger.wrapper import get_call_stats
from DKS_math.solver import *
from DKS_math.logger.logger import logger, logging_context, setup_logging

class ConfGDHSolver(ConfGDH):
    def __init__(self, stage_list:List[Tuple[GdhInstance, int]], bound_dict: Dict[str, Tuple[np.ndarray, np.ndarray, float]], t_in=288, avo_t_in=288, avo_dp=0.06):
        super().__init__(stage_list, t_in, avo_t_in, avo_dp)
        self.solver = Solver(self, bound_dict)


    def get_list_conf_gdh_solver(self) -> List['ConfGDHSolver']: 
        list_gpa_max = list(product(*list([
                list(range(1, cnt+1))
            for _, cnt in self.stage_list])))
        res = []
        for cnt in list_gpa_max:
            comp = self.clone()
            comp.stage_list = [
                (spch,cnt[ind])
            for ind, (spch,_) in enumerate(comp.stage_list)]
            res.append(comp)
        return res
    

    def clone(self)->'ConfGDHSolver':
        return copy.deepcopy(self)
    
    async def async_get_min_value(self, mode:Mode):
        res = []
        loop = asyncio.get_running_loop()
        list_comp = self.get_list_conf_gdh_solver()
        # with logging_context():
        with ProcessPoolExecutor() as pool: 
            tasks = [
                loop.run_in_executor(pool, comp.solver.minimize, mode)
            for comp in list_comp]
            min_value_list = await asyncio.gather(*tasks)
            pool.shutdown(wait=True)
        
        res = [
            comp.get_summry_without_bound(mode, min_val.x)
        for min_val, comp in zip(min_value_list, list_comp)
            if min_val.success
        ]
        df_res = pd.DataFrame([
            {**stage, 'stage_num': i, 'count_ind': ind} 
            for ind, result in enumerate(res)
            for i, stage in enumerate(result) 
        ]).set_index(['stage_num','count_ind'])

        df_res = df_res.unstack('count_ind').stack(level=0).T
        # df_res = pd.concat([
        #     pd.DataFrame(item.stack()).T
        # for item in res]).reset_index(drop=True)

        df_res = df_res[((df_res.loc[:, (df_res.columns.levels[0][-1], 'p_out')] - mode.p_target) < 0.75) & 
                        ((df_res.loc[:, (df_res.columns.levels[0][-1], 'p_out')] - mode.p_target) > -0.1)] #отбор по таргету 
        
        work_gpa_sum = df_res.loc[:, (slice(None), 'work_gpa')].sum(axis=1).min() #поиск минимального количества агрегатов на ступенях
        
        df_res = df_res[df_res.loc[:, (slice(None), 'work_gpa')].sum(axis=1) == work_gpa_sum] #поиск минимального количества агрегатов на ступенях - индекс
        idx_min = (df_res.loc[:, (slice(None), 'power')] * 
                   df_res.loc[:, (slice(None), 'work_gpa')].to_numpy()).sum(axis=1).idxmin() #поиск минимальной суммарной мощности на ступенях
        df_res:pd.Series = df_res.loc[idx_min]

        return df_res.unstack()
    

    async def get_calc_work_mode(self, mode:Mode) -> pd.DataFrame:
        df_conf_solv:pd.DataFrame = await self.async_get_min_value(mode)
        df_res = pd.concat([df_conf_solv])
        df_res = df_res.assign(
            q_rate=mode.q_rate,
            p_in=mode.p_in,
            p_target=mode.p_target
        )
        return df_res

# cProfile.run("grad_target(mode)", sort="cumtime")

if __name__ == '__main__':
    df_conf = []
    conf_solv_obj = ConfGDHSolver([
            (GdhInstance.create_by_csv('./DKS_math/Test/spch_dimkoef/ГПА-ц3-16С-45-1.7(ККМ).csv'), 4),
            (GdhInstance.create_by_csv('./DKS_math/Test/spch_dimkoef/CGX-425-16-65-1.7СМП(ПСИ).csv'), 4),
            ],
            bound_dict
            )

    q_rate = [25.32]
    p_in = [1.54]
    p_out = [4.80]
    print(time.strftime('%X'))
    beg = dt.now()
    for q_rate, p_in, p_out in list(zip(q_rate, p_in, p_out)):

        mode = Mode([q_rate, q_rate], p_in, 288, 512, 1.31, p_out, 0.101325, 283)
        
        df_conf_solv:pd.DataFrame = asyncio.run(conf_solv_obj.async_get_min_value(mode)) 
        df_conf.append(df_conf_solv)

    df_res = pd.concat(df_conf)
    print(df_res)
    print(dt.now() - beg)
    # print(get_call_stats())



 
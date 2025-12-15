from collections import defaultdict
import concurrent
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from itertools import product
import cProfile
import asyncio
import copy
import time
from datetime import datetime as dt
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from app_name.DKS_math.solver.solver_p_in import PressInSolver
from app_name.DKS_math.solver.solver_p_out import *

class ConfGDHSolver(ConfGDH):
    def __init__(self, comp_list:List[List[Tuple[GdhInstance, int]]], 
                 bound_dict_list: List[List[Dict[str, Tuple[np.ndarray, np.ndarray, float]]]], 
                 t_in=288, avo_t_in=288, avo_dp=0.06):
        
        super().__init__(comp_list[0], t_in, avo_t_in, avo_dp)
        self.solver = Solver(self, bound_dict_list[0])
        self.add_solvers = [
            ConfGDHSolver([stage_list], [bound_dict], t_in, avo_t_in, avo_dp)
            for stage_list, bound_dict in zip(comp_list[1:], bound_dict_list[1:])
        ]

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
    

    def get_summ(self, min_value_list, list_comp:List['ConfGDHSolver'], mode: Mode):

        res = [
            comp.get_summry_without_bound(mode, min_val.x)
        for min_val, comp in zip(min_value_list, list_comp)
            if min_val.success
        ]   

        if not res:
            return None
        
        df_res = pd.DataFrame([
            {**stage, 'stage_num': i, 'count_ind': ind} 
            for ind, result in enumerate(res)
            for i, stage in enumerate(result) 
        ]).set_index(['stage_num','count_ind'])

        df_res = df_res.unstack('count_ind').stack(level=0).T
        df_res = df_res[((df_res.loc[:, (df_res.columns.levels[0][-1], 'p_out')] - mode.p_target) < 0.75) & 
                        ((df_res.loc[:, (df_res.columns.levels[0][-1], 'p_out')] - mode.p_target) > -0.1)] #отбор по таргету 
        
        if df_res.empty:
            return None
        
        work_gpa_sum = df_res.loc[:, (slice(None), 'work_gpa')].sum(axis=1).min() #поиск минимального количества агрегатов на ступенях
        
        df_res = df_res[df_res.loc[:, (slice(None), 'work_gpa')].sum(axis=1) == work_gpa_sum] #поиск минимального количества агрегатов на ступенях - индекс

        idx_min = (df_res.loc[:, (slice(None), 'power')] * 
                   df_res.loc[:, (slice(None), 'work_gpa')].to_numpy()).sum(axis=1).idxmin() #поиск минимальной суммарной мощности на ступенях
        df_res = df_res.loc[idx_min]
        df_res:pd.DataFrame = df_res.unstack()
        
        df_res = df_res.assign(
            q_rate=mode.q_rate,
            p_in=mode.p_in,
            p_target=mode.p_target
        )
        return df_res  


    async def async_get_min_value(self, mode:Mode):
        list_comp = self.get_list_conf_gdh_solver()

        with ThreadPoolExecutor(max_workers=2) as pool: 
            loop = asyncio.get_running_loop()
            tasks = [
                loop.run_in_executor(pool, comp.solver.minimize, mode)
            for comp in list_comp
            ]
            min_value_list = await asyncio.gather(*tasks)

        return await self.get_summ(min_value_list, list_comp, mode)


    def sync_get_min_value(self, mode:Mode):
        list_comp = self.get_list_conf_gdh_solver()
        min_value_list = []
        for comp in list_comp:
            result = comp.solver.minimize(mode)
            min_value_list.append(result)

        return self.get_summ(min_value_list, list_comp, mode)


    def get_all_comp(self, modes):
        solvers = [self] + self.add_solvers
        results = defaultdict(list)
        for ind, solver in enumerate(solvers):
            for mode in modes:
                tasks = solver.sync_get_min_value(mode)
                results[ind].append(tasks)
        return results   

def calc_modes_parall(conf_solv_obj: ConfGDHSolver, modes: List[Mode]):
    results = conf_solv_obj.get_all_comp(modes)
    return results




 

import asyncio
from collections import defaultdict
from multiprocessing import Pool
import multiprocessing
import time
import concurrent
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Union
from itertools import product
from app_name.DKS_math.DKS import ConfGDHSolver
from app_name.DKS_math.solver.solver_p_in import PressInSolver
from app_name.DKS_math.solver.solver_p_out import *
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class ConfGDHSolverVfp(ConfGDHSolver):
    def __init__(self, comp_list:List[List[Tuple[GdhInstance, int]]], 
                 bound_dict_list:List[List[Dict[str, Tuple[np.ndarray, np.ndarray, float]]]], 
                 t_in=288, avo_t_in=288, avo_dp=0.06):
        super().__init__(comp_list, bound_dict_list, t_in, avo_t_in, avo_dp)
        self.solver = PressInSolver(self, bound_dict_list[0])
        self.bound_dict = bound_dict_list
        self.add_solvers = [
            ConfGDHSolverVfp([stage_list], [bound_dict], t_in, avo_t_in, avo_dp)
            for stage_list, bound_dict in zip(comp_list[1:], bound_dict_list[1:])
        ]

    def get_summ(self, min_value_list, list_comp:List['ConfGDHSolver'], mode: Mode):
        result = [
            comp.get_summry_without_bound(Mode(
                                        q_rate=mode.q_rate,
                                        p_in=min_val.x[0], 
                                        t_in=mode.t_in,
                                        r_value=mode.r_value,
                                        k_value=mode.k_value,
                                        p_target=mode.p_target,
                                        press_conditonal=mode.press_conditonal,
                                        temp_conditonal=mode.temp_conditonal), min_val.x[1:])
        for min_val, comp in zip(min_value_list, list_comp)
            if min_val.success
        ]   
        if not result:
            return None
    
        df_res = pd.DataFrame([
            {**stage, 'stage_num': i, 'count_ind': ind} 
            for ind, res in enumerate(result)
            for i, stage in enumerate(res) 
        ]).set_index(['stage_num','count_ind']).round(2)

        df_res = df_res.unstack('count_ind').stack(level=0).T

        work_gpa_sum = df_res.loc[:, (slice(None), 'work_gpa')].sum(axis=1).min() #поиск минимального количества агрегатов на ступенях
        
        df_res = df_res[df_res.loc[:, (slice(None), 'work_gpa')].sum(axis=1) == work_gpa_sum] #поиск минимального количества агрегатов на ступенях - индекс

        
        idx_min = (df_res.loc[:, (slice(None), 'power')] * 
                   df_res.loc[:, (slice(None), 'work_gpa')].to_numpy()).sum(axis=1).idxmin() #поиск минимальной суммарной мощности на ступенях
        df_res = df_res.loc[idx_min]
        df_res:pd.DataFrame = df_res.unstack()
        
        df_res = df_res.assign(
            q_rate=mode.q_rate,
            p_target=mode.p_target
        )

        return df_res.round(2)
    

    def get_all_comp(self, modes):
        solvers = [self] + self.add_solvers
        results = defaultdict(list)
        for ind, solver in enumerate(solvers):
            for mode in modes:
                tasks = solver.sync_get_min_value(mode)
                results[ind].append(tasks)
        return results


# def calc_table_vfp_param(conf_solv_obj: ConfGDHSolverVfp, table_params, bound_dict):
#     table_param = list(product(*table_params.values()))
#     extra_bounds = bound_dict[0]['extra_bounds']
#     modes = [Mode(  
#                 q_rate=param[0],
#                 p_in=None,
#                 t_in=extra_bounds['t_in']['value'],
#                 r_value=extra_bounds['r_value']['value'],
#                 k_value=extra_bounds['k_value']['value'],
#                 p_target=param[1],
#                 press_conditonal=extra_bounds['press_conditonal']['value'],
#                 temp_conditonal=extra_bounds['temp_conditonal']['value']
#             ) for param in table_param]
#     results = conf_solv_obj.get_all_comp(modes)
#     return results



def calc_table_vfp_param(conf_solv_obj: ConfGDHSolverVfp, table_params, bound_dict_arr):
    table_param = list(product(*table_params.dict().values()))
    extra_bounds = bound_dict_arr[0][0].dict()['extra_bounds']
    modes = [Mode(  
                q_rate=param[0],
                p_in=None,
                t_in=extra_bounds['t_in']['value'],
                r_value=extra_bounds['r_value']['value'],
                k_value=extra_bounds['k_value']['value'],
                p_target=param[1],
                press_conditonal=extra_bounds['press_conditonal']['value'],
                temp_conditonal=extra_bounds['temp_conditonal']['value']
            ) for param in table_param]
    results = conf_solv_obj.get_all_comp(modes)

    return results
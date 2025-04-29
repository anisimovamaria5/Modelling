import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from scipy.optimize import minimize, minimize_scalar, Bounds, NonlinearConstraint
from .solver import *
from itertools import product
import cProfile
import nest_asyncio
nest_asyncio.apply()
import asyncio
import copy
import time
from concurrent.futures import ProcessPoolExecutor

bound_dict = {
    'power':(
        np.array([16000, 16000]),
        np.array([7000, 7000]),
        200),
    'comp':(
        np.array([1.9, 1.9]),
        np.array([1, 1]),
        0.01),
    'udal':(
        np.array([100, 100]),
        np.array([0, 0]),
        1.0),    
    'freq_dimm':(
        np.array([1.05, 1.05]),    
        np.array([0.7, 0.7]),
        0.01),
    'p_out':(
        np.array([4.5, 6.5]),    
        np.array([0.1, 0.1]),
        0.1),
    'target':(
        np.array([10, 10]),    
        np.array([-10, -10]),
        0.1),
}

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
        with ProcessPoolExecutor() as pool: 
            tasks = [
                loop.run_in_executor(pool, comp.solver.minimize, mode)
            for comp in list_comp]
        
        min_value_list = await asyncio.gather(*tasks)
        res = [
                comp.get_summry_without_bound(mode, min_val.x)
        for min_val, comp in zip(min_value_list, list_comp)
            if min_val.success
            ]

        df_res = pd.concat([
            pd.DataFrame(item.stack()).T
        for item in res]).reset_index(drop=True)
        
        df_res = df_res[((df_res.loc[:, (df_res.columns.levels[0][-1], 'p_out')] - mode.p_target) < 0.75) & 
                        ((df_res.loc[:, (df_res.columns.levels[0][-1], 'p_out')] - mode.p_target) > -0.1)] #отбор по таргету 

        min_val = df_res.loc[:, (slice(None), 'work_gpa')].sum(axis=1).min() #поиск минимального количества агрегатов на ступенях
        df_res = df_res[df_res.loc[:, (slice(None), 'work_gpa')].sum(axis=1) == min_val] #поиск минимального количества агрегатов на ступенях - индекс
        
        idx_min = (df_res.loc[:, (slice(None), 'power')] * df_res.loc[:, (slice(None), 'work_gpa')].to_numpy()).sum(axis=1).idxmin() #поиск минимальной суммарной мощности на ступенях
        df_res:pd.Series = df_res.loc[idx_min]
        return df_res.unstack()
    

    def get_calc_work_mode(self, mode:Mode) -> pd.DataFrame:
        df_conf = []
        df_conf_solv:pd.DataFrame = asyncio.run(self.async_get_min_value(mode)) 
        df_conf.append(df_conf_solv)
        df_res = pd.concat(df_conf)
        return df_res


if __name__ == '__main__':
    conf_solv_obj = ConfGDHSolver([
            (GdhInstance.create_by_csv('./DKS_math/Test/spch_dimkoef/ГПА-ц3-16С-45-1.7(ККМ).csv'), 4),
            (GdhInstance.create_by_csv('./DKS_math/Test/spch_dimkoef/CGX-425-16-65-1.7СМП(ПСИ).csv'), 4),
            ],
            bound_dict
            )
    mode = Mode(34.6247653881433, 3.09655498953779, 288, 512, 1.31, 4.52460708334446)
    df = conf_solv_obj.get_calc_work_mode(mode)
    print(df)

    # q_rate = [47.32]
    # p_in = [1.54]
    # p_out = [4.80]
    # print(time.strftime('%X'))
    # for q_rate, p_in, p_out in list(zip(q_rate, p_in, p_out)):

    #     mode = Mode(q_rate, p_in, 288, 512, 1.31, p_out)
        
    #     df_conf_solv:pd.DataFrame = asyncio.run(conf_solv_obj.async_get_min_value(mode)) 
    #     df_conf.append(df_conf_solv)

    # df_res = pd.concat(df_conf)
    # print(df_res)
    # print(time.strftime('%X'))
 
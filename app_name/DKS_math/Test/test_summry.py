import pytest
from typing import List, Dict, Tuple
import pandas as pd
from ..DKS import *
import os
import numpy as np


def parse_case(f_name_case:str) -> Tuple[Mode, ConfGDHSolver, pd.DataFrame]:
    df_case = pd.read_csv(f"./DKS_math/Test/Fixture/{f_name_case}", sep='\t')

    p_in = float(df_case.loc[1]['0'])
    q_rate = float(df_case.loc[3]['0'])
    p_target = float(df_case.loc[2]['0'])
    t_in = float(df_case.loc[5]['0'])
    r_value = float(df_case.loc[4]['0'])
    k_value = float(df_case.loc[0]['0'])

    cnt_gpa_max = df_case.loc[18, ['0','1']]
    cnt_gpa_max_int = pd.to_numeric(cnt_gpa_max, downcast='signed')
    name_spch = df_case.loc[23, ['0','1']]

    bound_comp = df_case.loc[6:7, ['0','1']].values
    bound_freq = df_case.loc[8:9, ['0','1']].values
    bound_p_out = df_case.loc[10:11, ['0','1']].values
    bound_power = df_case.loc[12:13, ['0','1']].values
    bound_target = df_case.loc[14:15, ['0','1']].values
    bound_udal = df_case.loc[16:17, ['0','1']].values
    bound_dict = {'comp':(*bound_comp.astype('float'), 0.01), 
                  'freq_dimm':(*bound_freq.astype('float'), 0.01),
                  'p_out':(*bound_p_out.astype('float'), 0.1), 
                  'power':(*bound_power.astype('float'), 200), 
                  'target':(*bound_target.astype('float'), 0.1), 
                  'udal':(*bound_udal.astype('float'), 1)}
    
    conf = ConfGDHSolver(        
        stage_list = [
            (GdhInstance.create_by_csv(f'./DKS_math/Test/spch_dimkoef/{name.strip()}.csv'), cnt)
        for name, cnt in zip(name_spch, cnt_gpa_max_int)],
        bound_dict=bound_dict
    )

    power = df_case.loc[19, ['0','1']]
    cnt_gpa = df_case.loc[20, ['0','1']]
    freq = df_case.loc[25, ['0','1']]
    df_res_case = pd.DataFrame([freq, power, cnt_gpa], index=['freq', 'power', 'work_gpa'], dtype=float).T
    mode = Mode(q_rate=q_rate, p_in=p_in, p_target=p_target, t_in=t_in, r_value=r_value, k_value=k_value)

    return mode, conf, df_res_case


def get_cases() -> List[Tuple[Mode, ConfGDHSolver, pd.DataFrame]]:
    list_case = []
    for f_name in os.listdir("DKS_math\Test\Fixture"):
        list_case.append(parse_case(f_name))
    return list_case


@pytest.mark.parametrize('mode, conf, df_res_case', get_cases())
def test_summry(mode:Mode, conf:ConfGDHSolver, df_res_case:pd.DataFrame):
    
    df_res = conf.get_calc_work_mode(mode)
    df_res = df_res.loc[:,['freq','power','work_gpa']]
    df_res_case.index = df_res_case.index.astype(int)

    assert (abs(df_res_case.loc[:,'freq'] - df_res.loc[:,'freq']) <= 250).all() 
    assert (abs(df_res_case.loc[:,'power'] - df_res.loc[:,'power']) <= 600).all() 
    assert ((df_res_case.loc[:,'work_gpa'] - df_res.loc[:,'work_gpa']) == 0).all() 










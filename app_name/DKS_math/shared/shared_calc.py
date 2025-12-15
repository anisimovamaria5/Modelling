from typing import Sequence
from app_name.DKS_math.solver.solver_p_out import *
from app_name.DKS_math.DKS_vfp import ConfGDHSolverVfp, calc_table_vfp_param
from app_name.DKS_math.DKS import ConfGDHSolver, calc_modes_parall
from app_name.infrastructure.repositories.compressor.models.models_gdh import EqCompressorUnit


async def calc_vfp(
                lst_params_all_comp: List[list[Sequence[EqCompressorUnit]]],
                cnt_arr: List[list[int]],
                table_params: Dict,
                bound_dict: List[List[Dict]],
                deg:int
                ):
    
    #создаем экземпляр класса со всеми копоновками
    conf_solv_obj = ConfGDHSolverVfp([
        [
            (GdhInstance.read_dict(params[0], deg), cnt)
            for params, cnt in zip(lst_params_comp, lst_comp)
        ] 
            for lst_params_comp, lst_comp in zip(lst_params_all_comp, cnt_arr)
    ],
    bound_dict
    ) 
    #расчет всех режимов
    results = calc_table_vfp_param(conf_solv_obj, table_params, bound_dict)
    df_bif = [pd.concat(res) for res in results.values()]

    lst_with_df, lst_table_start, lst_table_middle = [], [], []
    for x in range(len(df_bif)):

        df_name = df_bif[x]['title'].iloc[0]
        df_filt = df_bif[x].loc[df_bif[x].index == 0]

        pivot_table = df_filt.pivot_table(
        values='p_in',
        index='q_rate',
        columns='p_target',
        aggfunc='first'
        )
        pivot_table_middle = _create_pivot_middle_table(pivot_table)
        
        pivot_table_clean = pivot_table.replace({np.nan: None})
        pivot_table_middle_clean = pivot_table_middle.replace({np.nan: None})  
        
        lst_with_df.append((df_name, pivot_table_middle_clean))
        lst_table_start.append(_format_table_dict(df_name, pivot_table_clean))
        lst_table_middle.append(_format_table_dict(df_name, pivot_table_middle_clean))
    
    #исходная таблица
    df_bif_serializable = [
        {
            'data': df.where(pd.notna(df), None).to_dict('records'),
            'columns': df.columns.tolist()
        }
        for df in df_bif
    ]

    #таблица vfp
    df_vfp = _create_table_vfp(lst_with_df)
    df_vfp_clean = df_vfp.replace({np.nan: None})

    #итоговый словарь со всеми таблицами
    dct = {
        'Big_table': df_bif_serializable,
        'Table_start': lst_table_start,
        'Table_middle': lst_table_middle,
        'Table_vfp': _format_table_dict('Table_vfp', df_vfp_clean)
    }
    print(df_vfp)
    return dct


def _create_pivot_middle_table(pivot_table: pd.DataFrame) -> pd.DataFrame:
    rows_len, columns_len = pivot_table.shape

    pivot_table_middle = pd.DataFrame(np.full((rows_len, columns_len), np.nan), columns=pivot_table.columns, index=pivot_table.index)
    pivot_table_middle.iloc[-1, -1] = pivot_table.iloc[-1, -1]
    
    for i in reversed(range(rows_len - 1)):
        if pd.notna(pivot_table.iloc[i, -1]) or pd.notna(pivot_table_middle.iloc[i+1, -1]):
            pivot_table_middle.iloc[i, -1] = np.nanmin([pivot_table.iloc[i, -1], 
                                                    pivot_table_middle.iloc[i+1, -1]])
        
        for j in reversed(range(columns_len - 1)):
            if pd.notna(pivot_table.iloc[-1, j]) or pd.notna(pivot_table_middle.iloc[-1, j+1]):
                pivot_table_middle.iloc[-1, j]  = np.nanmin([pivot_table.iloc[-1, j], 
                                                            pivot_table_middle.iloc[-1, j+1]])
            
            if pd.notna(pivot_table_middle.iloc[i+1, j]) or pd.notna(pivot_table_middle.iloc[i, j+1]) or pd.notna(pivot_table.iloc[i, j]):
                pivot_table_middle.iloc[i, j] = np.nanmin([pivot_table_middle.iloc[i+1, j], 
                                                        pivot_table_middle.iloc[i, j+1],
                                                        pivot_table.iloc[i, j]])
    return pivot_table_middle


def _format_table_dict(df_name:str, df:pd.DataFrame)-> Dict:
    return {
        df_name: df.to_dict(),
        'index': df.index.tolist(),
        'columns': df.columns.tolist()
    }


def _create_table_vfp(lst_with_df: List[Tuple[str, pd.DataFrame]]) -> pd.DataFrame:
    all_idx = sorted({idx for _, df in lst_with_df for idx in df.index})
    all_cols = sorted({idx for _, df in lst_with_df for idx in df.columns})
    all_eq = [name for name, _ in lst_with_df]

    vfp_table = pd.DataFrame(index=all_idx, columns=all_cols)
    for press in all_cols:
        df_press = pd.DataFrame(index=all_idx, columns=all_eq)
        for eq_name, df in lst_with_df:
            if press in df.columns:
                for idx in all_idx:
                    if idx in df.index:
                        df_press.at[idx, eq_name] = df.at[idx, press]
                        
        vfp_table[press] = df_press.min(axis=1, skipna=True)
    return vfp_table


def calc_vfp_2(
                csv_paths_arr,
                cnt_arr,
                table_params,
                bound_dict,
                ):
    conf_solv_obj = ConfGDHSolverVfp([
            [
                (GdhInstance.create_by_csv(csv_path_str), cnt)
                for csv_path_str, cnt in zip(paths, lst_cnt)
            ] 
                for paths, lst_cnt in zip(csv_paths_arr, cnt_arr)
        ],
        bound_dict
        )
    df = calc_table_vfp_param(conf_solv_obj, table_params, bound_dict)
    return df


async def calc_of_modes(
                lst_params_all_comp: List[list[Sequence[EqCompressorUnit]]],
                cnt_arr: List[list[int]],
                modes: List[Dict],
                bound_dict: List[List[Dict]],
                deg: int
                ):
    #создаем экземпляр класса со всеми копоновками

    conf_solv_obj = ConfGDHSolver([
        [
            (GdhInstance.read_dict(params[0], deg), cnt)
            for params, cnt in zip(lst_params_comp, lst_comp)
        ] 
            for lst_params_comp, lst_comp in zip(lst_params_all_comp, cnt_arr)
    ],
    bound_dict
    ) 
    
    mode = [Mode(**mode.dict()) for mode in modes]
    results = calc_modes_parall(conf_solv_obj, mode)
    df_bif = [pd.concat(res) for res in results.values()]
    return df_bif


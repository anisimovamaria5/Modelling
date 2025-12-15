import asyncio
import time
from datetime import datetime as dt

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from DKS_math.shared.shared_calc import calc_vfp_2

csv_paths_arr = [
                  ['./DKS_math/Test/spch_dimkoef/ГПА16 76-1.44.csv'],
                  ['./DKS_math/Test/spch_dimkoef/СПЧ 76-1,7 (3 ст Комс).csv'],
                  ['./DKS_math/Test/spch_dimkoef/ГПА 16-76 2.2.csv'],
                  ['./DKS_math/Test/spch_dimkoef/СПЧ 76-3.0 (Губа).csv'],
                  ['./DKS_math/Test/spch_dimkoef/ГПА 16-41-2.2.csv',
                   './DKS_math/Test/spch_dimkoef/СПЧ 76-3.0 (Губа).csv']
                 ]
              
cnt_arr = [
        [10],
        [10],
        [10],
        [10],
        [5,5]
        ]

table_param = {
                "q_rate": list(range(20,120,5)),
                "p_target": np.arange(6,7.5,.1)
              }
bound_dict = [
{
  "bounds": {
    "p_out_diff": {
      "name": "Превышение предельного давления",
      "short_name": "Pпред",
      "dimen": "МПа",
      "disable": False,
      "min_value": 0.1,
      "max_value": 7.7,
      "sensitivity": 0.1,
      "precision": 0
    },
    "freq_dimm": {
      "name": "Нормированная частота",
      "short_name": "Норм. част.",
      "dimen": "д.ед.",
      "disable": False,
      "min_value": 0.1,
      "max_value": 1.05,
      "sensitivity": 0.01,
      "precision": 2
    },
    "power": {
      "name": "Мощность",
      "short_name": "Мощь.",
      "dimen": "кВт",
      "disable": False,
      "min_value": 7000,
      "max_value": 16000,
      "sensitivity": 200,
      "precision": 0
    },
    "comp": {
      "name": "Степень сжатия",
      "short_name": "Степ. сж.",
      "dimen": "д.ед.",
      "disable": False,
      "min_value": 1,
      "max_value": 3.5,
      "sensitivity": 0.01,
      "precision": 2
    },
    "udal": {
      "name": "Удаленность",
      "short_name": "Удал.",
      "dimen": "д.ед.",
      "disable": False,
      "min_value": 0,
      "max_value": 100,
      "sensitivity": 1,
      "precision": 0
    }
  },
  "extra_bounds": {
    "k_value": {
      "name": "Коэффициент политропы",
      "short_name": "Коэф-т политропы",
      "dimen": "д.ед.",
      "disable": False,
      "value": 1.31
    },
    "t_in": {
      "name": "Температура начала процесса сжатия",
      "short_name": "Твх",
      "dimen": "К",
      "disable": False,
      "value": 288
    },
    "r_value": {
      "name": "Постоянная Больцмана поделенная на молярную массу",
      "short_name": "R",
      "dimen": "Дж/(кг*К)",
      "disable": False,
      "value": 512
    },
    "press_conditonal": {
      "name": "Давление стандартное",
      "short_name": "Pст",
      "dimen": "МПа",
      "disable": False,
      "value": 0.101325
    },
    "temp_conditonal": {
      "name": "Температура стандартная",
      "short_name": "Тст",
      "dimen": "К",
      "disable": False,
      "value": 283
    }
  }
},
{
  "bounds": {
    "p_out_diff": {
      "name": "Превышение предельного давления",
      "short_name": "Pпред",
      "dimen": "МПа",
      "disable": False,
      "min_value": 0.1,
      "max_value": 7.7,
      "sensitivity": 0.1,
      "precision": 0
    },
    "freq_dimm": {
      "name": "Нормированная частота",
      "short_name": "Норм. част.",
      "dimen": "д.ед.",
      "disable": False,
      "min_value": 0.1,
      "max_value": 1.05,
      "sensitivity": 0.01,
      "precision": 2
    },
    "power": {
      "name": "Мощность",
      "short_name": "Мощь.",
      "dimen": "кВт",
      "disable": False,
      "min_value": 7000,
      "max_value": 16000,
      "sensitivity": 200,
      "precision": 0
    },
    "comp": {
      "name": "Степень сжатия",
      "short_name": "Степ. сж.",
      "dimen": "д.ед.",
      "disable": False,
      "min_value": 1,
      "max_value": 3.5,
      "sensitivity": 0.01,
      "precision": 2
    },
    "udal": {
      "name": "Удаленность",
      "short_name": "Удал.",
      "dimen": "д.ед.",
      "disable": False,
      "min_value": 0,
      "max_value": 100,
      "sensitivity": 1,
      "precision": 0
    }
  },
  "extra_bounds": {
    "k_value": {
      "name": "Коэффициент политропы",
      "short_name": "Коэф-т политропы",
      "dimen": "д.ед.",
      "disable": False,
      "value": 1.31
    },
    "t_in": {
      "name": "Температура начала процесса сжатия",
      "short_name": "Твх",
      "dimen": "К",
      "disable": False,
      "value": 288
    },
    "r_value": {
      "name": "Постоянная Больцмана поделенная на молярную массу",
      "short_name": "R",
      "dimen": "Дж/(кг*К)",
      "disable": False,
      "value": 512
    },
    "press_conditonal": {
      "name": "Давление стандартное",
      "short_name": "Pст",
      "dimen": "МПа",
      "disable": False,
      "value": 0.101325
    },
    "temp_conditonal": {
      "name": "Температура стандартная",
      "short_name": "Тст",
      "dimen": "К",
      "disable": False,
      "value": 283
    }}}]

def plot_shared_calc(csv_paths_arr, 
                            cnt_arr,
                            table_param,
                            bound_dict):
  
  exl = pd.ExcelWriter('./media/Таблицы.xlsx') 
  results = calc_vfp_2(csv_paths_arr, cnt_arr, table_param, bound_dict)
  # print(results)
  # df_bif = pd.concat(results)
  df_bif = [pd.concat(res) for res in results.values()]

  for x in range(len(df_bif)):
    df_filt = df_bif[x].loc[df_bif[x].index == 0]
    pivot_table = df_filt.pivot_table(
      values='p_in',
      index='q_rate',
      columns='p_target',
      aggfunc='first'
    )
    rows_len = len(pivot_table)
    columns_len = len(pivot_table.columns)

    pivot_table_new = pd.DataFrame(np.full((rows_len, columns_len), np.nan), columns=pivot_table.columns, index=pivot_table.index)
    pivot_table_new.iloc[-1, -1] = pivot_table.iloc[-1, -1]
    
    for i in reversed(range(rows_len - 1)):
      if pd.notna(pivot_table.iloc[i, -1]) or pd.notna(pivot_table_new.iloc[i+1, -1]):
        pivot_table_new.iloc[i, -1] = np.nanmin([pivot_table.iloc[i, -1], 
                                                 pivot_table_new.iloc[i+1, -1]])
        
      for j in reversed(range(columns_len - 1)):
        if pd.notna(pivot_table.iloc[-1, j]) or pd.notna(pivot_table_new.iloc[-1, j+1]):
          pivot_table_new.iloc[-1, j]  = np.nanmin([pivot_table.iloc[-1, j], 
                                                    pivot_table_new.iloc[-1, j+1]])
        
        if pd.notna(pivot_table_new.iloc[i+1, j]) or pd.notna(pivot_table_new.iloc[i, j+1]) or pd.notna(pivot_table.iloc[i, j]):
          pivot_table_new.iloc[i, j] = np.nanmin([pivot_table_new.iloc[i+1, j], 
                                                  pivot_table_new.iloc[i, j+1],
                                                  pivot_table.iloc[i, j]])
      
    pivot_table.to_excel(exl, sheet_name=f'табл. {x} комп.')
    df_bif[x].to_excel(exl, sheet_name=f'общ. табл. {x} комп.')
    pivot_table_new.to_excel(exl, sheet_name=f'конечн. табл. {x} комп.')
  return exl.close()


if __name__ == "__main__":
    print(time.strftime('%X'))
    beg = dt.now()
    # print(asyncio.run(plot_shared_calc(csv_paths_arr, cnt_arr, table_param, bound_dict)))
    print(plot_shared_calc(csv_paths_arr, cnt_arr, table_param, bound_dict))

    print(dt.now() - beg)


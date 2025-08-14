from functools import wraps
import numpy as np
import pandas as pd
from DKS_math.logger.logger import logger
from datetime import datetime as dt
from functools import wraps
import logging
from datetime import datetime as dt
from typing import Any, Callable, Dict

filterList = [
    'get_',
    'func_z'
]

class LoggerClass:
    def __getattribute__(self, name: str) -> Any:
        attr = super().__getattribute__(name)

        if callable(attr) and any(line in name for line in filterList):
            @wraps(attr)
            def wrapped(*args, **kwargs):
                start_time = dt.now().timestamp()
                try:
                    result = attr(*args, **kwargs)
                    end_time = dt.now().timestamp()
                    duration = (end_time - start_time)
                    logger.info(f"{name}\t{duration:.6f}")
                    return result
                except Exception as e:
                    end_time = dt.now().timestamp()
                    logger.error(f"ERROR\t{name}: {str(e)}")
                    raise
            
            return wrapped
        
        return attr
    

def get_call_stats(log_file: str = 'DKS_math/logger/logs/app.csv') -> Dict[str, int]:
    with open(log_file, 'r') as f:
        lines = f.readlines()
    data = []
    valid_funcs = {
        'get_bound_dict_constr',
        'get_non_linear_freq_constr',
        'get_comp_constr',
        'func_z',
        'get_summry_without_bound',
        'get_freq_bound_all', 
        'get_summry_stage',
        'get_freq_bound',
        'create_by_csv',
        'get_volume_rate_from_press_temp',
        'get_u_val',
        'get_koef_rash_from_volume_rate',
        'get_nap',
        'get_kpd',
        'get_dh',
        'get_power',
        'get_comp_ratio',
        'get_pltn',
        'get_z_val'
    }
    
    for line in lines:
        if '\t' not in line:
            continue
        parts = line.strip().split('\t')
        if len(parts) != 2:
            continue
        name, duration = parts
        if name not in valid_funcs:
            continue
        try:
            duration = float(duration)
        except ValueError:
            continue 
        
        data.append({'name': name, 'duration': duration})

    df = pd.DataFrame(data)
    df_agg = df.groupby('name', as_index=False)['duration'].sum()
    
    with pd.option_context('display.max_rows', None):
        print(df_agg)
    
    total_time = df_agg['duration'].sum()
    print(f"\nTotal time: {total_time:.6f}")
    
    return df_agg.set_index('name')['duration'].to_dict()

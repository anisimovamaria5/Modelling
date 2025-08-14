from DKS_math.solver import *
from DKS_math.DKS import ConfGDHSolver


async def calc_of_modes(
                lst_params,
                lst_cnt,
                mode,
                bound_dict,
                deg
                ):
    conf_solv_obj = ConfGDHSolver([
                (GdhInstance.read_dict(params[0], deg), cnt)
                for params, cnt in zip(lst_params, lst_cnt)
                ],
                bound_dict
        )
    mode = Mode(**mode.dict())
    df = await conf_solv_obj.get_calc_work_mode(mode)
    return df
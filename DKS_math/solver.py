import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from scipy.optimize import minimize, minimize_scalar, Bounds, NonlinearConstraint
from .confGDH import *
import warnings
warnings.filterwarnings("ignore")

class Solver:

    def __init__(self, conf:ConfGDH, bound_dict:Dict[str,Tuple[np.ndarray,np.ndarray,float]]) -> None:
        self.conf = conf
        self.bound_dict = bound_dict

  
    def func_z(self, x, mode:Mode):        
        df_res = self.conf.get_summry_without_bound(mode, x)
        target = df_res['target'].iloc[-1]
        # print(df_res)
        # arr_bnd = np.array(self.bound_dict['power'][:-1])
        # power_w = abs((df_res['power'] - arr_bnd[1]) / (arr_bnd[0] - arr_bnd[1]))
        # power_w = [0,0] if np.all(abs((df_res['power'] - arr_bnd[1]) / (arr_bnd[0] - arr_bnd[1])).to_numpy() <= np.ones((2))) else power_w
        return target
    

    def get_2stage_targer_surface(self, mode:Mode):
        freq_bounds = self.conf.get_freq_bound_all(mode)
        freq_rehsaped = np.array([
            np.array([
                freq.reshape(-1)
            for _ in range(2**(len(freq_bounds)-1-ind))]).reshape(-1)
        for ind, freq in enumerate(freq_bounds)])
        freq_dop = self.conf.get_freq_dop(mode, freq_bounds)
        
        x_dop = 700
        dimens = np.array([50,50])
        x_arr = np.array(np.meshgrid(np.linspace(freq_rehsaped[0,0]-x_dop, freq_rehsaped[0,1]+x_dop, dimens[0]), np.linspace(freq_rehsaped[1,1]-x_dop, freq_rehsaped[1,2]+x_dop, dimens[1]))).reshape(2,dimens[0]*dimens[1]).T
        f_z = lambda x: self.conf.get_summry_without_bound(mode, x)
        z_ar = [f_z(x) for x in x_arr]
        freq1, freq2 = np.meshgrid(np.linspace(freq_rehsaped[0,0]-x_dop, freq_rehsaped[0,1]+x_dop, dimens[0]), np.linspace(freq_rehsaped[1,1]-x_dop, freq_rehsaped[1,2]+x_dop, dimens[1]))
        freq1_1, freq2_1 = freq_rehsaped[0], freq_rehsaped[1]
        x2, y2 =  np.linspace(freq_rehsaped[0,0], freq_rehsaped[0,1], dimens[0]), freq_dop[0]
        x4, y4 = np.linspace(freq_rehsaped[0,0], freq_rehsaped[0,1], dimens[1]), freq_dop[1]
        list_names = ['power', 'comp', 'freq_dimm', 'p_out', 'target']
        fig, axs = plt.subplots(nrows=len(list_names), ncols=2, figsize=(30,30))
        
        res = self.minimize(mode)
        
        for ind, name in enumerate(list_names):
            for stage_ind in [0,1]:
                ax = axs[ind,stage_ind]
                z_curr = np.array([z_val[name].iloc[stage_ind] for z_val in z_ar])
                z_curr = z_curr.reshape(*dimens)
                levels = np.linspace(
                        self.bound_dict[name][1][stage_ind],
                        self.bound_dict[name][0][stage_ind],
                        20) if name in self.bound_dict.keys() else None
                c = ax.contour(freq1, freq2, z_curr,levels=levels)
                ax.axis([freq1.min(), freq1.max(), freq2.min(), freq2.max()])
                ax.plot(x2, y2, markersize = 3, color = 'red')
                ax.plot(x4, y4, markersize = 3, color = 'red')
                ax.vlines(freq1_1[0], freq2_1[0], freq2_1[2], color = 'red')
                ax.vlines(freq1_1[1], freq2_1[1], freq2_1[3], color = 'red')
                ax.scatter(np.array([res.x[0]]), np.array([res.x[1]]), s=50, c='red')
                fig.colorbar(c, ax=ax)
                ax.clabel(c, inline=True, fontsize=10) 
                ax.set_title(name)
        return ax
    

    def get_non_linear_constr(self, freqs:np.ndarray, mode:Mode):
        curr_mode = mode.clone()
        curr_mode.q_rate = mode.q_rate / self.conf.stage_list[0][1]
        freq_min, freq_max = self.conf.stage_list[0][0].get_freq_bound(curr_mode.get_volume_rate)
        res = [(freqs[0] - freq_min) / (freq_max - freq_min)]
        for ind, (stage, cnt_gpa)  in list(enumerate(self.conf.stage_list))[1:]:
            curr_mode.p_in = self.conf.stage_list[ind-1][0].get_summry(curr_mode, freqs[ind-1])['p_out'] - self.conf.avo_dp
            curr_mode.q_rate = mode.q_rate / cnt_gpa
            freq_min, freq_max = stage.get_freq_bound(curr_mode.get_volume_rate)
            res.append((freqs[ind] - freq_min) / (freq_max - freq_min))
        return res
    

    def get_non_linear_constr2(self, freqs:np.ndarray, mode:Mode):
        res = self.conf.get_summry_without_bound(mode, freqs)['comp']
        return res.tolist()
    

    def get_non_linenar_constr3(self, mode:Mode, num_stage) -> List[NonlinearConstraint]:
        fun = lambda x: self.conf.get_summry_without_bound(mode, x).loc[num_stage, self.bound_dict.keys()].to_numpy().T.tolist()
        bound_arrs = np.array([item[:-1] for item in self.bound_dict.values()])
        constr_obj = NonlinearConstraint(fun=fun, lb=bound_arrs[:, 1, num_stage].tolist(), ub=bound_arrs[:, 0, num_stage].tolist())
        return constr_obj
    

    def minimize(self, mode:Mode):
        freq_bounds = self.conf.get_freq_bound_all(mode)
        freq_rehsaped = np.array([
            np.array([
                freq.reshape(-1)
            for _ in range(2**(len(freq_bounds)-1-ind))]).reshape(-1)
        for ind, freq in enumerate(freq_bounds)])
        bounds = Bounds(
            [min(freq_rehsaped[0]), min(freq_rehsaped[1])],
            [max(freq_rehsaped[0]), max(freq_rehsaped[1])]
            )

        res = minimize(self.func_z, 
                        x0=np.array([np.mean(freq_rehsaped[0]), np.mean(freq_rehsaped[1])]),
                        args=(mode),
                        # x0=freq_rehsaped[:,0] * np.array([1.1]*2),
                        # x0=np.array([5300,5300]),
                        method='SLSQP',
                        bounds=bounds, 
                        constraints=[
                            NonlinearConstraint(lambda x: self.get_non_linear_constr(x, mode), lb=np.array([0,0]), ub=np.array([1,1])),
                            NonlinearConstraint(lambda x: self.get_non_linear_constr2(x, mode), lb=1, ub=np.inf),
                            *[
                                self.get_non_linenar_constr3(mode, ind)
                            for ind, _ in enumerate(self.conf.stage_list)]
                        ]
                        )
        return res
          

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

if __name__ == '__main__':
    conf_obj = ConfGDH([
            (GdhInstance.create_by_csv('./DKS_math/Test/spch_dimkoef/ГПА-ц3-16С-45-1.7(ККМ).csv'), 1),
            (GdhInstance.create_by_csv('./DKS_math/Test/spch_dimkoef/CGX-425-16-65-1.7СМП(ПСИ).csv'), 2),
        ])
    mode = Mode(34.6247653881433, 3.09655498953779, 288, 512, 1.31, 4.52460708334446)
    solv = Solver(conf_obj, bound_dict)
    # solv.get_2stage_targer_surface(mode)
    # plt.show()
    res = solv.minimize(mode)
    print(res)
    # print(conf_obj.get_summry_without_bound(mode, res.x))
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from scipy.optimize import minimize, Bounds, NonlinearConstraint
from app_name.DKS_math.confGDH import *
import warnings
from autograd import value_and_grad
import autograd.numpy as anp
# from logger.wrapper import LoggerClass
warnings.filterwarnings("ignore")


class Solver:

    def __init__(self, conf:ConfGDH, bound_dict:Dict[str,Tuple[np.ndarray,np.ndarray,float]]) -> None:
        self.conf = conf
        self.bound_dict = bound_dict


    def func_z(self, x, mode:Mode):    
        df_res = self.conf.get_summry_without_bound(mode, x)
        target = df_res[-1]['target']
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
        x_arr = np.array(np.meshgrid(np.linspace(freq_rehsaped[0,0]-x_dop, freq_rehsaped[0,1]+x_dop, dimens[0]), 
                                     np.linspace(freq_rehsaped[1,1]-x_dop, freq_rehsaped[1,2]+x_dop, dimens[1]))).reshape(2,dimens[0]*dimens[1]).T
        f_z = lambda x: self.conf.get_summry_without_bound(mode, x)
        z_ar = [f_z(x) for x in x_arr]
        freq1, freq2 = np.meshgrid(np.linspace(freq_rehsaped[0,0]-x_dop, freq_rehsaped[0,1]+x_dop, dimens[0]), 
                                   np.linspace(freq_rehsaped[1,1]-x_dop, freq_rehsaped[1,2]+x_dop, dimens[1]))
        freq1_1, freq2_1 = freq_rehsaped[0], freq_rehsaped[1]
        x2, y2 =  np.linspace(freq_rehsaped[0,0], freq_rehsaped[0,1], dimens[0]), freq_dop[0]
        x4, y4 = np.linspace(freq_rehsaped[0,0], freq_rehsaped[0,1], dimens[1]), freq_dop[1]
        list_names = ['power', 'comp', 'freq_dimm', 'p_out_diff', 'target']
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
    

    def get_freq_constr(self, freqs:np.ndarray, mode:Mode):
        curr_mode = mode.clone()
        curr_mode.q_rate = mode.q_rate[0] / self.conf.stage_list[0][1]
        freq_min, freq_max = self.conf.stage_list[0][0].get_freq_bound(curr_mode.get_volume_rate)
        res = [(freqs[0] - freq_min) / (freq_max - freq_min)]
        for ind, (stage, cnt_gpa)  in list(enumerate(self.conf.stage_list))[1:]:
            curr_mode.p_in = self.conf.stage_list[ind-1][0].get_summry_stage(curr_mode, freqs[ind-1])['p_out'] - self.conf.avo_dp
            curr_mode.q_rate = mode.q_rate[ind] / cnt_gpa
            freq_min, freq_max = stage.get_freq_bound(curr_mode.get_volume_rate)
            res.append((freqs[ind] - freq_min) / (freq_max - freq_min))  
        return res


    def get_comp_constr(self, freqs:np.ndarray, mode:Mode):
        res = self.conf.get_summry_without_bound(mode, freqs)
        return [stage['comp'] for stage in res]
    

    def get_bound_dict_constr(self, mode:Mode, num_stage) -> List[NonlinearConstraint]:
        param_names = ['p_out_diff', 'freq_dimm', 'power', 'comp', 'udal']
        bounds_array_staged = np.array([
            [
                [getattr(stage.bounds, name).max_value, getattr(stage.bounds, name).min_value]
                for name in param_names
            ]

            for stage in self.bound_dict
        ]
        )
        fun = lambda x: [self.conf.get_summry_without_bound(mode, x)[num_stage][key] 
                        for key in param_names]
        constr_obj = NonlinearConstraint(
                                fun=fun, 
                                lb=bounds_array_staged[num_stage][:, 1].tolist(), 
                                ub=bounds_array_staged[num_stage][:, 0].tolist()
                                )
        # keys = self.bound_dict.keys()
        # values = self.bound_dict.values()
        # fun = lambda x: [self.conf.get_summry_without_bound(mode, x)[num_stage][key] 
        #                 for key in keys]
        # bound_arrs = np.array([item[:-1] for item in values])
        # constr_obj = NonlinearConstraint(
        #                         fun=fun, 
        #                         lb=bound_arrs[:, 1, num_stage].tolist(), 
        #                         ub=bound_arrs[:, 0, num_stage].tolist()
        #                         )
        return constr_obj
    

    def minimize(self, mode:Mode):
        num_stages = len(self.conf.stage_list)
        freq_bounds = self.conf.get_freq_bound_all(mode)
        freq_rehsaped = np.array([
            np.array([
                freq.reshape(-1)
            for _ in range(2**(len(freq_bounds)-1-ind))]).reshape(-1)
        for ind, freq in enumerate(freq_bounds)])
        lower_bounds = [min(freq_rehsaped[i]) for i in range(num_stages)]
        upper_bounds = [max(freq_rehsaped[i]) for i in range(num_stages)]
        bounds = Bounds(lower_bounds, upper_bounds)
        constraints = [
                NonlinearConstraint(lambda x: self.get_freq_constr(x, mode), 
                                    lb=np.zeros(num_stages), 
                                    ub=np.ones(num_stages)),
                NonlinearConstraint(lambda x: self.get_comp_constr(x, mode), 
                                    lb=1, 
                                    ub=np.inf),
                *[
                    self.get_bound_dict_constr(mode, ind)
                for ind, _ in enumerate(self.conf.stage_list)
                ]
            ] 
        
       # x0 = np.array([np.mean(freq_rehsaped[i]) for i in range(num_stages)])  
        x0 = np.array((bounds.lb + bounds.ub) / 2)  
        res = minimize(self.func_z, 
                        x0=x0,
                        args=(mode),
                        method='SLSQP',
                        bounds=bounds, 
                        constraints=constraints
                        )
        return res

    
bound_dict = {
    'power':(
        np.array([16000, 16000]),
        np.array([7000, 7000]),
        200),
    'comp':(
        np.array([3.0, 3.0]),
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
        np.array([4.5, 7.5]),    
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
    mode = Mode([34.6247, 34.6247], 3.09655498953779, 288, 512, 1.31, 4.52460708334446, 0.101325, 283)
    solv = Solver(conf_obj, bound_dict)
    # solv.get_2stage_targer_surface(mode)
    # plt.show()
    # res = solv.grad_target(mode) 
    res = solv.minimize(mode)
    print(res)
    print(conf_obj.get_summry_without_bound(mode, res.x))

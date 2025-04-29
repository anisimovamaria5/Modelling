"""Модуль ГДХ
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from .baseFormulas import BaseFormulas
from .mode import Mode
from typing import Tuple

class GdhInstance(BaseFormulas):

    @classmethod
    def create_by_csv(cls, csv_path_str) -> "GdhInstance":
        df = pd.read_csv(csv_path_str)
        diam = df['diam'].to_numpy()
        koef_rash = df['k_rash'].to_numpy()
        koef_nap = df['k_nap'].to_numpy()
        kpd = df['kpd'].to_numpy()
        freq_nom = df['fnom'].to_numpy()
        t_in = df['temp'].to_numpy()
        r_value = df['R'].to_numpy()
        k_value = df['k'].to_numpy()
        mgth = df['mgth'].to_numpy()
        stepen = df['stepen'].to_numpy()
        p_title = df['p_title'].to_numpy()
        return cls(diam[0], koef_nap, koef_rash, kpd, freq_nom[0], t_in[0], r_value[0], k_value[0], mgth[0], stepen[0], p_title[0], deg=4, name=csv_path_str)
    

    def __init__(self, diam, koef_nap, koef_rash, kpd, freq_nom, t_in, r_value, k_value, mgth, stepen, p_title, deg=4, name=None): 
        self.diam = diam
        self.koef_nap = koef_nap
        self.koef_rash = koef_rash 
        self.kpd = kpd 
        self.freq_nom = freq_nom
        self.t_in = t_in
        self.r_value = r_value
        self.k_value = k_value
        c00_nap = np.polyfit(x=koef_rash, y=koef_nap, deg=deg)
        self.f_nap = np.poly1d(c00_nap)
        c00_kpd = np.polyfit(x=koef_rash, y=kpd, deg=deg)        
        self.f_kpd = np.poly1d(c00_kpd)
        self.mgth = mgth
        self.stepen = stepen
        self.p_title = p_title
        self.name = name


    def get_freq_bound(self, volume_rate_arr) -> Tuple[float,float]:
        koef_rash_bound_arr = np.array([self.koef_rash.max(), self.koef_rash.min()])
        freq_bound_arr = 4 * volume_rate_arr / (math.pi**2 * self.diam**3 * koef_rash_bound_arr)
        return freq_bound_arr
    

    def get_summry(self, mode:Mode, freq:float|np.ndarray, t_in=None, r_value=None, k_value=None) -> pd.Series:
        t_in = self.t_in if t_in is None else t_in
        r_value = self.r_value if r_value is None else r_value
        k_value = self.k_value if k_value is None else k_value
        volume_rate = mode.get_volume_rate
        u_val = self.get_u_val(self.diam, freq)
        koef_rash_ = self.get_koef_rash_from_volume_rate(self.diam, u_val, volume_rate)
        koef_nap_ = self.f_nap(koef_rash_)
        kpd_ = self.f_kpd(koef_rash_)
        dh = self.get_dh(koef_nap_, u_val)
        power = self.get_power(mode.q_rate, dh, kpd_, r_value)
        comp = self.get_comp_ratio(mode.p_in, dh, r_value, t_in, k_value, kpd_)

        res = {
            'power':power,
            'comp':comp,
            'volume_rate':volume_rate,
            'udal':(koef_rash_ - self.koef_rash.min()) / (self.koef_rash.max() - self.koef_rash.min()) * 100,
            'freq':freq,
            'freq_dimm':freq / self.freq_nom,
            'p_in':mode.p_in,
            'p_out':mode.p_in * comp,
            'title':self.name,
            'target':abs(mode.p_in * comp - mode.p_target)
        }

        return pd.Series(res) 
      

    def __repr__(self) -> str:
        return f'{self.name}'
    

    def __format__(self, format_spec: str) -> str:
        return f'{self.mgth:.0f}-{self.p_title:.0f} {self.stepen}'
    

    def show_gdh(self):
        fig, ax = plt.subplots(figsize=(9, 5)) 
        ax.scatter(self.koef_rash, self.koef_nap, c='b')
        x2 = np.linspace(np.min(self.koef_rash), np.max(self.koef_rash), 100)
        ax.plot(x2, self.f_nap(x2), c='b')
        ax2 = ax.twinx()
        ax2.scatter(self.koef_rash, self.kpd, c='r')
        ax2.plot(x2, self.f_kpd(x2), c='r')
        return ax, ax2
    

if __name__ == '__main__':
    # gdh = GdhInstance.create_by_csv('spch_dimkoef\ГПА 16-41-2.2.csv')
    gdh = GdhInstance.create_by_csv('spch_dimkoef/ГПА-ц3-16С-45-1.7(ККМ).csv')
    mode = Mode(24.62, 3.1, 288, 512, 1.31, 4.52)
    print(gdh.get_summry(mode, 3500.3))
    # print(gdh.get_freq_bound(534))
    # ax, ax2 = gdh.show_gdh()
    # plt.show()

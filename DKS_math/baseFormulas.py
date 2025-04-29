"""Основные формулы
"""
import math
import numpy as np
class BaseFormulas:


    @classmethod
    def get_z_val(cls, p_in:float, t_in:float, t_krit=190, p_krit=4.6) -> float: 
        """Расчет коэффициента сверсжимаемости
        Args:
            p_in (float): Давление, МПА
            t_in (float): Температура, К
            t_krit (int, optional): Критич. Температура, К {default = 190}
            p_krit (float, optional): Критич. Давление, МПа {default = 4.6}
        Returns:
            float: Значение сверхсжимаемости Z
        """
        z_val = 1 - 0.427 * p_in / p_krit * (t_in / t_krit)**(-3.688)        
        if type(z_val) == float:
            return 0.1 if z_val < 0 else z_val
        else:
            if type(z_val) == np.ndarray or type(z_val) == np.float64:
                return np.where(z_val < 0 , 0.1, z_val)
            else:
                return z_val
    

    @classmethod 
    def get_pltn(cls, p_in:float, t_in:float, r_value:float, z:float) -> float: 
        """Расчет плотности
        Args:
            p_in (float): Давление, МПА
            t_in (float): Температура, K
            r_value (float): Постоянная Больцмана поделеная на молярную массу
            z (float): Коэффициент сверсжимаемости
        Returns:
            float: плотность газа при указанные давлении и температуры, кг/м3
        """
        pltn = p_in * 10**6 / (z * r_value * t_in)
        return pltn
    

    @classmethod
    def get_volume_rate_from_press_temp(cls, q_rate:float, p_in:float, t_in:float, r_value:float, press_conditonal:float, temp_conditonal:float) -> float:
        """Расчет объемного расхода
        Args:
            pltn_0 (float): Стандартная плотность, кг/м3
            q_rate (float): Комерческий расход, млн. м3/сут
            pltn_1 (float): Плотность, кг/м3
        Returns:
            float: Возвращяет обьемный расход, при указанных условиях, м3/мин
        """
        z_0 = cls.get_z_val(press_conditonal, temp_conditonal, t_krit=190, p_krit=4.6)
        pltn_0 = cls.get_pltn(press_conditonal, temp_conditonal, r_value, z_0)
        z_1 = cls.get_z_val(p_in, t_in, t_krit=190, p_krit=4.6)
        pltn_1 = cls.get_pltn(p_in, t_in, r_value, z_1)
        volume_rate = q_rate * 10**6 * pltn_0 / (24 * 60 * pltn_1)
        return volume_rate
    

    @classmethod 
    def get_u_val(cls, diam:float, freq:float) -> float:
        """Расчет угловой скорости
        Args:
            diam (float): Диаметр, м
            freq (float): Частота, об/мин
        Returns:
            float: Угловая скорость, м/с
        """
        u_val = freq * diam * math.pi / 60
        return u_val
    

    @classmethod
    def get_koef_rash_from_volume_rate(cls, diam:float, u_val:float, volume_rate:float) -> float:
        """Расчет коэффицента расхода
        Args:
            diam (float): Диаметр, м
            u_val (float): Угловая скорость, м/с
            volume_rate (float): Обьемный расход при заданных условиях, м3/мин
        Returns:
            float: Возвращяет коеффициент расхода при заданных условиях и текущей температуре, д.ед
        """
        koef_rash_ = 4 * volume_rate / (math.pi * diam**2 * u_val * 60) 
        return koef_rash_
    

    @classmethod 
    def get_dh(cls, koef_nap_:float, u_val:float) -> float:
        """удельное изменение энтальпии
        Args:
            koef_nap_ (float): Политропный кпд, д.ед
            u_val (float): Угловая скорость, м/с
        Returns:
            float: Необходимое для сжатия изменение энтальпии, дж/кг
        """
        dh =  koef_nap_ * u_val**2
        return dh
    

    @classmethod       
    def get_power(cls, q_rate:float, dh:float, kpd_:float, r_value:float, press_conditonal:float, temp_conditonal:float) -> float: 
        """Расчет мощности
        Args:
            dh (float): Изменение энтальпии, дж/кг
            m (float): Массовый расход, м3/с
            kpd_ (float): Политропный кпд, д.ед
        Returns:
            float: Мощность, кВт
        """
        z_0 = cls.get_z_val(press_conditonal, temp_conditonal, t_krit=190, p_krit=4.6)
        pltn_0 = cls.get_pltn(press_conditonal, temp_conditonal, r_value, z_0)
        m = q_rate * pltn_0 * 10**6 / 24 / 60 / 60 
        power = dh * m / kpd_ / 10**3
        return power
    

    @classmethod
    def get_comp_ratio(cls, p_in:float, dh:float, r_value:float, t_in:float, k_value:float, kpd_:float) -> float:
        """Расчет степени сжатия
        Args:
            m_t (float): Дробь с политропным кпд и коэффициентом политропы
            dh (float): Изменение энтальпии, дж/кг
            r_value (float): Газовая постоянная, Дж/(кг*К)
            z (float): Сверхсжимаемость, д.ед
            t_in (float): Температура на входе, К
        Returns:
            float: Степень сжатия, д.ед
        """
        m_t = (k_value - 1) / (k_value * kpd_)
        z = cls.get_z_val(p_in, t_in, t_krit=190, p_krit=4.6)
        comp_ratio = (dh * m_t / (z * r_value * t_in) + 1)**(1 / m_t)
        return comp_ratio
    
    
if __name__ == '__main__':
    print(BaseFormulas.get_comp_ratio(2,2,2,2,2))
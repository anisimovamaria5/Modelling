"""Основные формулы
"""
import numpy as np
# from DKS_math.logger.wrapper import LoggerClass

class BaseFormulas:
    _PI_OVER_60 = np.pi / 60


    @classmethod
    def get_z_val(cls, p_in:np.ndarray, t_in:np.ndarray, t_krit=190, p_krit=4.6) -> np.ndarray: 
        """Расчет коэффициента сверсжимаемости
        Args:
            p_in (np.ndarray): Давление, МПА
            t_in (np.ndarray): Температура, К
            t_krit (int, optional): Критич. Температура, К {default = 190}
            p_krit (float, optional): Критич. Давление, МПа {default = 4.6}
        Returns:
            np.ndarray: Значение сверхсжимаемости Z
        """
        z_val = 1 - 0.427 * p_in / p_krit * (t_in / t_krit)**(-3.688)
        if isinstance(z_val, (np.ndarray, np.float64)):
            return np.where(z_val < 0, 0.1, z_val)
        return 0.1 if z_val < 0 else z_val
    

    @classmethod 
    def get_pltn(cls, p_in:np.ndarray, t_in:np.ndarray, r_value:float, z:np.ndarray) -> np.ndarray: 
        """Расчет плотности
        Args:
            p_in (np.ndarray): Давление, МПА
            t_in (np.ndarray): Температура, K
            r_value (float): Постоянная Больцмана поделеная на молярную массу
            z (np.ndarray): Коэффициент сверсжимаемости
        Returns:
            np.ndarray: плотность газа при указанные давлении и температуры, кг/м3
        """
        return p_in * 10**6 / (z * r_value * t_in)  
    

    @classmethod
    def get_volume_rate_from_press_temp(cls, q_rate:np.ndarray, p_in:np.ndarray, t_in:np.ndarray, r_value:float, press_conditonal:float, temp_conditonal:float) -> np.ndarray:
        """Расчет объемного расхода
        Args:
            pltn_0 (np.ndarray): Стандартная плотность, кг/м3
            q_rate (np.ndarray): Комерческий расход, млн. м3/сут
            pltn_1 (np.ndarray): Плотность, кг/м3
        Returns:
            np.ndarray: Возвращяет обьемный расход, при указанных условиях, м3/мин
        """
        z_0 = cls.get_z_val(press_conditonal, temp_conditonal)
        pltn_0 = press_conditonal  / (z_0 * r_value * temp_conditonal) 
        z_1 = cls.get_z_val(p_in, t_in)
        pltn_1 = p_in / (z_1 * r_value * t_in)
        return q_rate * 10**6 * pltn_0 / (24 * 60 * pltn_1)  
    

    @classmethod 
    def get_u_val(cls, diam:float, freq:np.ndarray) -> np.ndarray:
        """Расчет угловой скорости
        Args:
            diam (float): Диаметр, м
            freq (np.ndarray): Частота, об/мин
        Returns:
            np.ndarray: Угловая скорость, м/с
        """
        return freq * diam * cls._PI_OVER_60
    

    @classmethod
    def get_koef_rash_from_volume_rate(cls, diam:float, u_val:np.ndarray, volume_rate:np.ndarray) -> np.ndarray:
        """Расчет коэффицента расхода
        Args:
            diam (float): Диаметр, м
            u_val (np.ndarray): Угловая скорость, м/с
            volume_rate (np.ndarray): Обьемный расход при заданных условиях, м3/мин
        Returns:
            np.ndarray: Возвращяет коеффициент расхода при заданных условиях и текущей температуре, д.ед
        """
        return 4 * volume_rate / (np.pi * diam**2 * u_val * 60) 
    

    @classmethod 
    def get_dh(cls, koef_nap_:np.ndarray, u_val:np.ndarray) -> np.ndarray:
        """Расчет удельного изменения энтальпии
        Args:
            koef_nap_ (np.ndarray): Политропный кпд, д.ед
            u_val (np.ndarray): Угловая скорость, м/с
        Returns:
            np.ndarray: Необходимое для сжатия изменение энтальпии, дж/кг
        """
        return koef_nap_ * u_val**2
    

    @classmethod       
    def get_power(cls, q_rate:np.ndarray, dh:np.ndarray, kpd_:np.ndarray, r_value:float, press_conditonal:float, temp_conditonal:float) -> np.ndarray: 
        """Расчет мощности
        Args:
            dh (np.ndarray): Изменение энтальпии, дж/кг
            m (np.ndarray): Массовый расход, м3/с
            kpd_ (np.ndarray): Политропный кпд, д.ед
        Returns:
            np.ndarray: Мощность, кВт
        """
        z_0 = cls.get_z_val(press_conditonal, temp_conditonal, t_krit=190, p_krit=4.6)
        pltn_0 = cls.get_pltn(press_conditonal, temp_conditonal, r_value, z_0)
        m = q_rate * pltn_0 * 10**6 / 24 / 60 / 60 
        return dh * m / kpd_ / 10**3
    

    @classmethod
    def get_comp_ratio(cls, p_in:np.ndarray, dh:np.ndarray, r_value:float, t_in:np.ndarray, k_value:float, kpd_:np.ndarray) -> np.ndarray:
        """Расчет степени сжатия
        Args:
            m_t (np.ndarray): Дробь с политропным кпд и коэффициентом политропы
            dh (np.ndarray): Изменение энтальпии, дж/кг
            r_value (float): Газовая постоянная, Дж/(кг*К)
            k_value (float): Коэффициент политропы, д.ед
            z (np.ndarray): Сверхсжимаемость, д.ед
            t_in (np.ndarray): Температура на входе, К
        Returns:
            np.ndarray: Степень сжатия, д.ед
        """
        m_t = (k_value - 1) / (k_value * kpd_)
        z = cls.get_z_val(p_in, t_in, t_krit=190, p_krit=4.6)
        return (dh * m_t / (z * r_value * t_in) + 1)**(1 / m_t)
    

    @classmethod       
    def get_p_in(cls, q_rate:np.ndarray, kpd_:np.ndarray, r_value:float, 
                 press_conditonal:float, temp_conditonal:float, power:np.ndarray, 
                 k_value:float, p_in:np.ndarray, t_in:np.ndarray, p_out:np.ndarray) -> np.ndarray: 
        """Расчет давления

        Args:
            q_rate (np.ndarray): Комерческий расход, млн. м3/сут
            dh (np.ndarray): Изменение энтальпии, дж/кг
            kpd_ (np.ndarray): Политропный кпд, д.ед
            r_value (float): Газовая постоянная, Дж/(кг*К)
            press_conditonal (float): Стандартное давление, МПа
            temp_conditonal (float): Стандартная температура, К
            power (np.ndarray): Мощность, кВт
            k_value (float): Коэффициент политропы, д.ед
            p_in (np.ndarray): Давление на входе, МПа
            t_in (np.ndarray): Температура на входе, К
            p_out (np.ndarray): Давление на выходе, МПа

        Returns:
            np.ndarray: Давление на входе, МПа
        """
        z_0 = cls.get_z_val(press_conditonal, temp_conditonal, t_krit=190, p_krit=4.6)
        pltn_0 = cls.get_pltn(press_conditonal, temp_conditonal, r_value, z_0)
        z_1 = cls.get_z_val(p_in, t_in)
        m = q_rate * pltn_0 * 10**6 / 24 / 60 / 60 
        m_t = (k_value - 1) / (k_value)
        comp = ((power * 10**3 * kpd_ * m_t) / (m * z_1 * r_value * t_in) + 1)**(1 / m_t)
        return p_out / comp * 10


if __name__ == '__main__':
    print(BaseFormulas.get_comp_ratio(2,2,2,2,2))
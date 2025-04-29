""" Входные данные
"""
from .baseFormulas import BaseFormulas

class Mode(BaseFormulas):

    def __init__(self, q_rate:float, p_in:float, t_in:float, r_value:float, k_value:float, p_target:float) -> None:
        self.q_rate = q_rate
        self.p_in = p_in
        self.t_in = t_in
        self.r_value = r_value
        self.k_value = k_value
        self.p_target = p_target


    def __repr__(self) -> str:
        return f'{self.__dict__}'
    

    def clone(self):
        return Mode(**self.__dict__)
    
    @property
    def get_volume_rate(self):
        return self.get_volume_rate_from_press_temp(self.q_rate, self.p_in, self.t_in, self.r_value, press_conditonal=0.101325, temp_conditonal=283)
    

    def __truediv__(self,other):
        res = self.clone()
        res.q_rate /= other
        return res
    
    
if __name__=='__main__':
    mode_obj = Mode(1,2,300,4,5,6)
    print(mode_obj)
    print(mode_obj.get_volume_rate)
    mode_obj /= 2
    print(mode_obj)
    # print(mode_obj.get_volume_rate)


     

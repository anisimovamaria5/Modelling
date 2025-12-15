from mode import Mode
class SolutionFreqBoundError(Exception):
    def __init__(self, mode:Mode):
        self.mode = mode
    def __str__(self):
        return f'Ошибка граничных условий по частоте с {self.mode}'

def f_test(mode):
    raise SolutionFreqBoundError(mode)

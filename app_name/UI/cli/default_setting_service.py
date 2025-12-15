from pathlib import Path
import configparser


class DefaultSettingService:

    def __init__(self, setting_path: Path):
        self.setting_path = setting_path
        self.config = configparser.ConfigParser()
        self.config.read(setting_path)


    def default_params(self):
        if 'default_params' in self.config:
            param = {}
            for key in self.config['default_params']:
                value = self.config['default_params'][key]
                if value.isdigit():
                    param[key] = int(value)
                else:
                    param[key] = float(value)
            return param
        

    def bound_params(self):
        if 'bound_dict' in self.config:
            param = {}
            for key in self.config['bound_dict']:
                value = self.config['bound_dict'][key]
                if value.isdigit():
                    param[key] = int(value)
                else:
                    param[key] = float(value)
                
            return param

if __name__ == '__main__':
    a = DefaultSettingService('setting.ini')
    print(a.bound_params())
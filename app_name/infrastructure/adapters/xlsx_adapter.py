import pandas as pd
from pathlib import Path


class ExcelDataAdapter:

    def save_result_in_excel(data, output_path:Path):
        """Сохранение результатов в эксель"""
        if isinstance(data, pd.DataFrame):
            data.to_excel(output_path)

        elif isinstance(data, list):
            df = pd.DataFrame(data)
            df.to_excel(output_path)

        elif isinstance(data, dict):
            # Если есть несколько таблиц, сохраняем на разные листы
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                
                for sheet, table_data in data.items():
                    
                    if isinstance(table_data, pd.DataFrame):
                        table_data.to_excel(writer, sheet_name=str(sheet), index=False)
                    
                    elif isinstance(table_data, list):
                        pd.DataFrame(table_data).to_excel(
                            writer, sheet_name=str(sheet), index=False
                        )
                    
                    elif isinstance(table_data, dict):
                        pd.DataFrame([table_data]).to_excel(
                            writer, sheet_name=str(sheet), index=False
                        )
        else:
            raise ValueError(f"Неподдерживаемый тип данных: {type(data)}")
        

    def get_data_from_excel(input_path:Path):
        """Получение данных из экселя и преобразование в нужный формат"""

        excel_file = pd.ExcelFile(input_path)
        sheet_names = excel_file.sheet_names

        if len(sheet_names) == 1:
            df = pd.read_excel(excel_file, sheet_name=sheet_names[0])
            return df.to_dict()
        
        else:
            result = {}
            for sheet_name in sheet_names:

                try:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    df_clean = df.where(pd.notnull(df), None)
                    result[sheet_name] = df_clean.to_dict('records')
                except Exception as e:
                    print(f'Ошибка в чтении листа {sheet_name}:{e}')
                    result[sheet_name] = None

        return result    
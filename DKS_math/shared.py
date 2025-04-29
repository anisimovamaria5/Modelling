from typing import List
import pandas as pd
import numpy as np
from DKS_math.dimKoef import DimKoef
from app.schemas.schemas import CurveResponse, Dataset, DataPoint

def get_df_by_excel(excel_data, deg=4, k_value=1.31, press_conditonal=0.101325, temp_conditonal=283) -> List[pd.DataFrame]:
    excel = pd.ExcelFile(excel_data)
    lst_df = []
    for sheet_name in excel.sheet_names:
        dimKoef = DimKoef.create_by_excel(
            excel, 
            sheet_name, 
            k_value=k_value, 
            deg=deg, 
            press_conditonal=press_conditonal, 
            temp_conditonal=temp_conditonal
        )
        df = dimKoef.create_df()
        df['name'] = sheet_name
        df['deg'] = deg
        df_1 = df[['k_rash', 'k_nap', 'kpd', 'k_nap_polin', 'kpd_polin', 'k_rash_lin', 'freq', 'deg', 'name']]
        # df_big = df[['diam', 'k_rash', 'k_nap', 'kpd', 'fnom', 'temp', 'R', 'k', 'mgth', 'stepen', 'p_title']]
        df_1 = df_1.fillna(0)
        lst_df.append(df_1)
    return lst_df

labels = ['polytropic efficiency', 'head coefficient']
kinds = ['points', 'line']
y_col_2 = {
    'polytropic efficiency': ['kpd_polin'],
    'head coefficient': ['k_nap_polin']
}
y_col_1 = {
    'kpd', 'k_nap'
}
# y_col_2 = {
#     'kpd_polin', 'k_nap_polin'
# }
def use_pydantic_model(lst_df):
    curves = []
    for i, df in enumerate(lst_df):
        datasets = []

        for kind in kinds:
            if kind == 'points':
                grouped_dfs = [group for _, group in df.groupby('freq')]
                for gr_df in grouped_dfs:
                    for label in labels:
                        for y in y_col_1:
                            dataset = Dataset(label=label, 
                                            title=f"freq={gr_df['freq'].iloc[0]}",
                                            kind=kind,
                                            data=[DataPoint(x=row['k_rash'], y=row[y]) for _, row in gr_df.iterrows()])                        
                            datasets.append(dataset)
            else:
                for label in labels:
                    for y in y_col_2[label]:
                        dataset = Dataset(label=label, 
                                        title=f"deg={df['deg'][0]}",
                                        kind=kind,
                                        data=[DataPoint(x=row['k_rash_lin'], y=row[y]) for _, row in df.iterrows()])                        
                        datasets.append(dataset)                
        curve = CurveResponse(datasets=datasets, label=df['name'][0])
        curves.append(curve)
    return curves


if __name__=='__main__':
    f_path = 'media\Оцифрованные СПЧ.xlsx'
    res = get_df_by_excel(f_path)
    print([
        (type(row['kpd']),type(row['k_rash']),type(row['k_nap']))
    for _, row in res[0].iterrows()])



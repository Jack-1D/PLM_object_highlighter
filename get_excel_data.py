'''
excel料號轉存在local variable

excel第一行必須是料號
'''
import pandas as pd

def excel_to_list(path: str, sheet_name: str):
    '''料號轉一維list'''
    df = pd.read_excel(path, sheet_name=sheet_name).iloc[:,[0]]
    object_list = df.values.tolist()
    flatten_list = lambda l : [flat for tmp in l for flat in flatten_list(tmp)] if type(l) == list else [l]

    flat_list = flatten_list(object_list)
    return flat_list
    # print(flat_list)
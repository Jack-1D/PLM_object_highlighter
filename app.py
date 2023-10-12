import pandas as pd

df = pd.read_excel("data_sheets/Cable Library Tool 202301.xlsm", sheet_name="Common parts").iloc[:,[0]]
object_list = df.values.tolist()
flatten_list = lambda l : [flat for tmp in l for flat in flatten_list(tmp)] if type(l) == list else [l]

flat_list = flatten_list(object_list)
print(flat_list)
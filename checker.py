'''
檢查各個料號是否在excel裡
'''
from get_excel_data import excel_to_list

def add_check_status(check_list: list, bom: list[dict]) -> None:
    '''添加status到BOM裡'''
    for item in bom:
        if item['itemNumber'] in check_list:
            item['status'] = 'exist'
        else:
            item['status'] = 'not_exist'
    return

def match_list(team: str) -> list:
    '''下拉式選單選擇使用的excel'''
    match team:
        case "cable":
            return excel_to_list("data_sheets/Cable Library Tool 202301.xlsm", "Common parts")
        case "other":
            return excel_to_list("data_sheets/Cable Library Tool 202301.xlsm", "Common parts")
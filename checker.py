'''
檢查各個料號是否在excel裡
'''
from get_excel_data import excel_to_list
import threading

def add_check_status(check_list: list, bom: list[dict]) -> None:
    '''添加status到BOM裡'''
    f = lambda bom_item : bom_item.update({'status':'exist'}) if bom_item['itemNumber'] in check_list else bom_item.update({'status':'not_exist'})
    threads = []
    for i in range(len(bom)):
        threads.append(threading.Thread(target=f, args=(bom[i],)))
        threads[i].start()
    for thread in threads:
        thread.join()
    return

def match_list(team: str) -> list:
    '''下拉式選單選擇使用的excel'''
    match team:
        case "cable":
            return excel_to_list("data_sheets/Cable Library Tool 202301.xlsm", "Common parts")
        case "other":
            return excel_to_list("data_sheets/活頁簿1.xlsx", "工作表1")
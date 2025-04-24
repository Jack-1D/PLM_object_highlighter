"""
input: team

output: 對應檔案最後修改日期
"""

import os
from datetime import datetime


def match_date(team: str = "") -> str:
    '''回傳檔案最後修改是多久以前'''
    match team:
        case "Screw":
            file_path = "data_sheets/ME screw common parts.xlsx"
        case "六角螺柱":
            file_path = "data_sheets/ME standoff common parts.xlsx"
        case "PCB SMD Nut":
            file_path = "data_sheets/ME pcb smt nut common parts.xlsx"
        case "Carton and Pizza box":
            file_path = "data_sheets/ME carton common parts.xlsx"
        case "TVS":
            file_path = "data_sheets/EMC component list.xlsx"
        case "GDT":
            file_path = "data_sheets/EMC component list.xlsx"
        case "Varistor":
            file_path = "data_sheets/EMC component list.xlsx"
        case "Bead":
            file_path = "data_sheets/EMC component list.xlsx"
        case "Common mode choke":
            file_path = "data_sheets/EMC component list.xlsx"
        case "安規電容":
            file_path = "data_sheets/EMC component list.xlsx"
        case "Gasket":
            file_path = "data_sheets/EMC component list.xlsx"
        case "Conductive tape":
            file_path = "data_sheets/EMC component list.xlsx"
        case "Ferrite core":
            file_path = "data_sheets/EMC component list.xlsx"
        case "AC/DC EMI filter":
            file_path = "data_sheets/EMC component list.xlsx"
        case "EMI spring":
            file_path = "data_sheets/EMC component list.xlsx"
        case "cable":
            file_path = "data_sheets/Cable Library Tool 202301.xlsm"
        case _:
            file_path = ""

    modification_time = os.path.getmtime(file_path)
    passed_time = int(datetime.now().timestamp() - modification_time)  
    final_date = ""
    if passed_time // 86400 != 0:
        final_date += str(passed_time // 86400) + "天 "
    passed_time %= 86400
    if passed_time // 3600 != 0:
        final_date += str(passed_time // 3600) + "小時 "
    passed_time %= 3600
    if passed_time // 60 != 0:
        final_date += str(passed_time // 60) + "分鐘 "
    passed_time %= 60
    if passed_time != 0:
        final_date += str(passed_time) + "秒 "
    final_date += "前"

    return final_date
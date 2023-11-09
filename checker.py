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
            return excel_to_list("Cable Library Tool 202301.xlsm", "Common parts"), ["^30\-.{5}\-.{4}\-.{2}$"]
        case "TVS":
            return excel_to_list("EMC component list.xlsx", "TVS"), ["^69\-91.{3}\-.{4}$", "^69\-00000\-.{4}$", "^69\-00000\-.{4}\-.{4}$", "^19\-91.{3}\-.{4}$"]
        case "GDT":
            return excel_to_list("EMC component list.xlsx", "GDT"), ["^69\-93.{3}\-.{4}$"]
        case "Varistor":
            return excel_to_list("EMC component list.xlsx", "Varistor"), ["^69\-700.{2}\-.{4}$"]
        case "Bead":
            return excel_to_list("EMC component list.xlsx", "Bead"), ["^68\-.{5}\-.{4}$"]
        case "Common mode choke":
            return excel_to_list("EMC component list.xlsx", "Common mode choke"), ["^68\-.{5}\-.{4}$"]
        case "安規電容":
            return excel_to_list("EMC component list.xlsx", "安規電容"), ["^12\-473.{2}\-.{4}$", "^12\-1051Z\-1.{3}$", "^78\-10228\-2C.{2}$", "^78\-.{4}E\-.{4}$", "^78\-.{4}9\-2.{3}$"]
        case "Gasket":
            return excel_to_list("EMC component list.xlsx", "Gasket"), ["^40\-00.{3}\-.{4}$", "^40\-00.{3}\-.{4}\-.{2}$"]
        case "Conductive tape":
            return excel_to_list("EMC component list.xlsx", "Conductive tape"), ["^40\-00.{3}\-.{4}$", "^40\-00.{3}\-.{4}\-.{2}$"]
        case "Ferrite core":
            return excel_to_list("EMC component list.xlsx", "Ferrite core"), ["^40\-3.{4}\-.{4}\-.{2}$"]
        case "AC/DC EMI filter":
            return excel_to_list("EMC component list.xlsx", "AC/DC EMI filter"), ["^30\-20416\-0.{3}$", "^30\-20481\-0.{3}$", "^30\-20383\-1.{3}$", "^30\-500.{2}\-.{4}$", "^30\-500.{2}\-.{4}\-.{2}$", "^04\-02050\-.{4}$", "^04\-50505\-.{4}$"]
        case "EMI spring":
            return excel_to_list("EMC component list.xlsx", "EMI spring"), ["^40\-200.{2}\-.{4}$", "^62\-800.{2}\-.{4}$"]
        case "Screw":
            return excel_to_list("screw.xlsx"), ["^33\-.{5}\-.{4}$", "^33\-.{5}\-.{4}\-.{2}$"]
        case "Carton":
            return excel_to_list("carton.xlsx"), ["^46\-10.{3}\-.{4}$", "^46\-10.{3}\-.{4}\-.{2}$"]
        case "other":
            return excel_to_list("活頁簿1.xlsx", "工作表1")
"""
檢查各個料號是否在excel裡

先對excel表格做regular expression
"""
from get_excel_data import excel_to_list
import threading, re


def add_check_status(check_list: list, bom: list[dict]) -> None:
    """添加status到BOM裡"""
    f = (
        lambda bom_item: bom_item.update({"status": "exist"})
        if bom_item["itemNumber"] in check_list
        else bom_item.update({"status": "not_exist"})
    )
    threads = []
    for i in range(len(bom)):
        threads.append(threading.Thread(target=f, args=(bom[i],)))
        threads[i].start()
    for thread in threads:
        thread.join()
    return


def match_list(team: str) -> list:
    """下拉式選單選擇使用的excel"""
    match team:
        case "cable":
            target = excel_to_list("Cable Library Tool 202301.xlsm", "Common parts")
            pattern = ["^30\-.{5}\-.{4}\-.{2}$"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "TVS":
            target = excel_to_list("EMC component list.xlsx", "TVS")
            pattern = [
                "^69\-91.{3}\-.{4}$",
                "^69\-00000\-.{4}$",
                "^69\-00000\-.{4}\-.{4}$",
                "^19\-91.{3}\-.{4}$",
            ]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "GDT":
            target = excel_to_list("EMC component list.xlsx", "GDT")
            pattern = ["^69\-93.{3}\-.{4}$"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "Varistor":
            target = excel_to_list("EMC component list.xlsx", "Varistor")
            pattern = ["^69\-700.{2}\-.{4}$"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "Bead":
            target = excel_to_list("EMC component list.xlsx", "Bead")
            pattern = ["^68\-.{5}\-.{4}$"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "Common mode choke":
            target = excel_to_list("EMC component list.xlsx", "Common mode choke")
            pattern = ["^68\-.{5}\-.{4}$"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "安規電容":
            target = excel_to_list("EMC component list.xlsx", "安規電容")
            pattern = [
                "^12\-473.{2}\-.{4}$",
                "^12\-1051Z\-1.{3}$",
                "^78\-10228\-2C.{2}$",
                "^78\-.{4}E\-.{4}$",
                "^78\-.{4}9\-2.{3}$",
            ]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "Gasket":
            target = excel_to_list("EMC component list.xlsx", "Gasket")
            pattern = [
                "^40\-00.{3}\-.{4}$",
                "^40\-00.{3}\-.{4}\-.{2}$",
            ]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "Conductive tape":
            target = excel_to_list("EMC component list.xlsx", "Conductive tape ")
            pattern = [
                "^40\-00.{3}\-.{4}$",
                "^40\-00.{3}\-.{4}\-.{2}$",
            ]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "Ferrite core":
            target = excel_to_list("EMC component list.xlsx", "Ferrite-core")
            pattern = ["^40\-3.{4}\-.{4}\-.{2}$"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "AC/DC EMI filter":
            target = excel_to_list("EMC component list.xlsx", "AC&DC EMI filter")
            pattern = [
                "^30\-20416\-0.{3}$",
                "^30\-20481\-0.{3}$",
                "^30\-20383\-1.{3}$",
                "^30\-500.{2}\-.{4}$",
                "^30\-500.{2}\-.{4}\-.{2}$",
                "^04\-02050\-.{4}$",
                "^04\-50505\-.{4}$",
            ]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "EMI spring":
            target = excel_to_list("EMC component list.xlsx", "EMI spring")
            pattern = [
                "^40\-200.{2}\-.{4}$",
                "^62\-800.{2}\-.{4}$",
            ]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "Screw":
            target = excel_to_list("ME screw common parts.xlsx")
            pattern = ["^33\-0", "^33\-1", "^33\-2", "^33\-6", "^33\-5"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "六角螺柱":
            target = excel_to_list("ME standoff common parts.xlsx")
            pattern = ["^33\-70", "^33\-71"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "PCB SMD Nut":
            target = excel_to_list("ME pcb smt nut common parts.xlsx")
            pattern = ["^33\-72", "^33\-73"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "Carton and Pizza box":
            target = excel_to_list("ME carton common parts.xlsx")
            pattern = ["^46\-1", "^46\-02", "^46\-2"]
            target = [
                t for t in target for p in pattern if re.search(p, str(t)) != None
            ]
            return target, pattern
        case "other":
            return excel_to_list("活頁簿1.xlsx", "工作表1")

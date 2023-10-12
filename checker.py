'''
檢查各個料號是否在excel裡
'''

def add_check_status(check_list: list, bom: list[dict]) -> None:
    for item in bom:
        if item['itemNumber'] in check_list:
            item['status'] = 'exist'
        else:
            item['status'] = 'not_exist'
    return
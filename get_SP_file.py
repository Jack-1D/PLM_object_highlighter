'''
取得Sharepoint上的excel檔，並抓到data_sheets裡

每10分鐘都會登入Sharepoint抓資料，如果抓錯了可以從console看出來
'''
from office365.sharepoint.client_context import ClientContext, UserCredential
from office365.sharepoint.files.file import File
import io
import pandas as pd
import os
import time
import logging
import re
from dotenv import load_dotenv, find_dotenv

def alive_get_SP_file():
    '''每10分鐘抓一次sharepoint檔案'''
    load_dotenv(find_dotenv())
    sp1_logger = logging.getLogger('main.sub_get_SP')
    sp1_logger.setLevel(logging.INFO)
    sp2_logger = logging.getLogger('main.sub_get_SP')
    sp2_logger.setLevel(logging.INFO)
    while True:
        # screw
        try:
            screwSheet = ["(十字)","(星型 Torx)","(內六角)","Thumb Screw","Spring Screw"]
            url = "https://ampro1.sharepoint.com/sites/TPDC%20Web%20Portal/PEC/MED"
            user_credentials = UserCredential(os.getenv('SP_USERNAME'),os.getenv('SP_PASSWORD'))
            ctx = ClientContext(url).with_credentials(user_credentials)
            file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/03_%E6%A9%9F%E6%A7%8B%E8%A8%AD%E8%A8%88/2024%20%E5%B8%B8%E7%94%A8%E8%9E%BA%E7%B5%B2(%E6%9F%B1)%E7%B8%BD%E8%A1%A8.xlsx"
            response = File.open_binary(ctx, file_url)
            bytes_file_obj = io.BytesIO()
            bytes_file_obj.write(response.content)
            bytes_file_obj.seek(0)
            df = pd.read_excel(bytes_file_obj, engine="openpyxl", sheet_name=None)
            combine = pd.Series(name="料號")
            for k in df.keys():
                for sheet in screwSheet:
                    if re.search(sheet, k) != None:
                        combine = pd.concat([combine, df[k]['TPE Part No.']], axis=0, ignore_index=True)
                        combine = pd.concat([combine, df[k]['SH Part No.']], axis=0, ignore_index=True)
            combine.name = '料號'
            print(f"Screw: {combine}")
            sp1_logger.info(f"Screw: {combine}")
            combine.to_excel('data_sheets/ME screw common parts.xlsx', index=False)
        except Exception as e:
            print(f"Error: {e}\n")

        # 六角銅柱
        try:
            url = "https://ampro1.sharepoint.com/sites/TPDC%20Web%20Portal/PEC/MED"
            user_credentials = UserCredential(os.getenv('SP_USERNAME'),os.getenv('SP_PASSWORD'))
            ctx = ClientContext(url).with_credentials(user_credentials)
            file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/03_%E6%A9%9F%E6%A7%8B%E8%A8%AD%E8%A8%88/2024%20%E5%B8%B8%E7%94%A8%E8%9E%BA%E7%B5%B2(%E6%9F%B1)%E7%B8%BD%E8%A1%A8.xlsx"  
            response = File.open_binary(ctx, file_url)
            bytes_file_obj = io.BytesIO()
            bytes_file_obj.write(response.content)
            bytes_file_obj.seek(0)
            df = pd.read_excel(bytes_file_obj, engine="openpyxl", sheet_name=None)
            combine = pd.Series(name="料號")
            for k in df.keys():
                if re.search("六角螺柱", k) != None:
                    df = df[k]
                    break
            combine = pd.concat([combine, df['TPE Part No.']], axis=0, ignore_index=True)
            combine = pd.concat([combine, df['SH Part No.']], axis=0, ignore_index=True)
            combine.name = '料號'
            print(f"六角螺柱: {combine}")
            sp1_logger.info(f"六角螺柱: {combine}")
            combine.to_excel('data_sheets/ME standoff common parts.xlsx', index=False)
        except Exception as e:
            print(f"Error: {e}\n")

        # PCB/SMD
        try:
            url = "https://ampro1.sharepoint.com/sites/TPDC%20Web%20Portal/PEC/MED"
            user_credentials = UserCredential(os.getenv('SP_USERNAME'),os.getenv('SP_PASSWORD'))
            ctx = ClientContext(url).with_credentials(user_credentials)
            file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/03_%E6%A9%9F%E6%A7%8B%E8%A8%AD%E8%A8%88/2024%20%E5%B8%B8%E7%94%A8%E8%9E%BA%E7%B5%B2(%E6%9F%B1)%E7%B8%BD%E8%A1%A8.xlsx"  
            response = File.open_binary(ctx, file_url)
            bytes_file_obj = io.BytesIO()
            bytes_file_obj.write(response.content)
            bytes_file_obj.seek(0)
            df = pd.read_excel(bytes_file_obj, engine="openpyxl", sheet_name=None)
            combine = pd.Series(name="料號")
            for k in df.keys():
                if re.search("PCB SMD Nut", k) != None:
                    df = df[k]
                    break
            combine = pd.concat([combine, df['TPE Part No.']], axis=0, ignore_index=True)
            combine = pd.concat([combine, df['SH Part No.']], axis=0, ignore_index=True)
            combine.name = '料號'
            print(f"PCB SMD Nut: {combine}")
            sp1_logger.info(f"PCB SMD Nut: {combine}")
            combine.to_excel(f'data_sheets/ME pcb smt nut common parts.xlsx', index=False)
        except Exception as e:
            print(f"Error: {e}\n")

        # carton & pizza box
        try:
            carton_pizzabox_sheet = ["Carton", "Box"]
            url = "https://ampro1.sharepoint.com/sites/TPDC%20Web%20Portal/PEC/MED"
            user_credentials = UserCredential(os.getenv('SP_USERNAME'),os.getenv('SP_PASSWORD'))
            ctx = ClientContext(url).with_credentials(user_credentials)
            file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/03_%E6%A9%9F%E6%A7%8B%E8%A8%AD%E8%A8%88/MED%20Carton,%20Box%20Dimension%20Search.xlsx"
            response = File.open_binary(ctx, file_url)
            bytes_file_obj = io.BytesIO()
            bytes_file_obj.write(response.content)
            bytes_file_obj.seek(0)
            df = pd.read_excel(bytes_file_obj, sheet_name=None, skiprows=1)
            combine = pd.Series(name="料號")
            for k in df.keys():
                for sheet in carton_pizzabox_sheet:
                    if re.search(sheet, k) != None:
                        if '台北料號' in df[k]:
                            combine = pd.concat([combine, df[k]['台北料號']], axis=0, ignore_index=True)
                            combine = pd.concat([combine, df[k]['上海料號']], axis=0, ignore_index=True)
                        else:
                            combine = pd.concat([combine, df[k]['料號']], axis=0, ignore_index=True)
                            combine = pd.concat([combine, df[k]['皆為兩地common part']], axis=0, ignore_index=True)
            combine.name = '料號'
            print(f"carton & pizza box: {combine}")
            sp2_logger.info(f"carton & pizza box: {combine}")
            combine.to_excel('data_sheets/ME carton common parts.xlsx', index=False)
        except Exception as e:
            print(f"Error: {e}\n")
        
        time.sleep(600)

if __name__ == "__main__":
    alive_get_SP_file()
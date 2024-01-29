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
        url = "https://ampro1.sharepoint.com/sites/TPDC%20Web%20Portal/PEC/MED"
        user_credentials = UserCredential(os.getenv('SP_USERNAME'),os.getenv('SP_PASSWORD'))
        ctx = ClientContext(url).with_credentials(user_credentials)
        file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/03_%E6%A9%9F%E6%A7%8B%E8%A8%AD%E8%A8%88/2021%20%E5%B8%B8%E7%94%A8%E8%9E%BA%E7%B5%B2(%E6%9F%B1)%E7%B8%BD%E8%A1%A8.xlsx"  
        response = File.open_binary(ctx, file_url)
        bytes_file_obj = io.BytesIO()
        bytes_file_obj.write(response.content)
        bytes_file_obj.seek(0)
        df = pd.read_excel(bytes_file_obj, engine="openpyxl", sheet_name=None)
        combine = pd.Series(name="料號")
        for k in df.keys():
            if re.search("Common Screw List", k) != None:
                df = df[k]
                break
        combine = pd.concat([combine, df['TPE Part No.']], axis=0, ignore_index=True)
        combine = pd.concat([combine, df['SH Part No.']], axis=0, ignore_index=True)
        combine.name = '料號'
        print(f"Screw: {combine}")
        sp1_logger.info(f"Screw: {combine}")
        combine.to_excel('data_sheets/screw.xlsx', index=False)

        # 六角銅柱
        url = "https://ampro1.sharepoint.com/sites/TPDC%20Web%20Portal/PEC/MED"
        user_credentials = UserCredential(os.getenv('SP_USERNAME'),os.getenv('SP_PASSWORD'))
        ctx = ClientContext(url).with_credentials(user_credentials)
        file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/03_%E6%A9%9F%E6%A7%8B%E8%A8%AD%E8%A8%88/2021%20%E5%B8%B8%E7%94%A8%E8%9E%BA%E7%B5%B2(%E6%9F%B1)%E7%B8%BD%E8%A1%A8.xlsx"  
        response = File.open_binary(ctx, file_url)
        bytes_file_obj = io.BytesIO()
        bytes_file_obj.write(response.content)
        bytes_file_obj.seek(0)
        df = pd.read_excel(bytes_file_obj, engine="openpyxl", sheet_name=None)
        for k in df.keys():
            if re.search("六角螺柱", k) != None:
                df = df[k]
                break
        print(f"六角螺柱: {df['料號']}")
        sp1_logger.info(f"六角螺柱: {df['料號']}")
        df = df['料號']
        df.to_excel('data_sheets/standoff.xlsx', index=False)

        # PCB/SMD
        url = "https://ampro1.sharepoint.com/sites/TPDC%20Web%20Portal/PEC/MED"
        user_credentials = UserCredential(os.getenv('SP_USERNAME'),os.getenv('SP_PASSWORD'))
        ctx = ClientContext(url).with_credentials(user_credentials)
        file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/03_%E6%A9%9F%E6%A7%8B%E8%A8%AD%E8%A8%88/2021%20%E5%B8%B8%E7%94%A8%E8%9E%BA%E7%B5%B2(%E6%9F%B1)%E7%B8%BD%E8%A1%A8.xlsx"  
        response = File.open_binary(ctx, file_url)
        bytes_file_obj = io.BytesIO()
        bytes_file_obj.write(response.content)
        bytes_file_obj.seek(0)
        df = pd.read_excel(bytes_file_obj, engine="openpyxl", sheet_name=None)
        for k in df.keys():
            if re.search("PCB SMD Nut", k) != None:
                df = df[k]
                break
        print(f"PCB SMD Nut: {df['料號']}")
        sp1_logger.info(f"PCB SMD Nut: {df['料號']}")
        df = df['料號']
        df.to_excel(f'data_sheets/smd nut.xlsx', index=False)

        # carton
        file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/MED%20Public/MED%20Carton,%20Box%20Dimension%20Search.xls"
        response = File.open_binary(ctx, file_url)
        bytes_file_obj = io.BytesIO()
        bytes_file_obj.write(response.content)
        bytes_file_obj.seek(0)
        df = pd.read_excel(bytes_file_obj, sheet_name=None, skiprows=1)
        combine = pd.Series(name="料號")
        for k in df.keys():
            if re.search("carton input data", k) != None:
                combine = pd.concat([combine, df[k]['料號']], axis=0, ignore_index=True)
        sp2_logger.info(f"carton: {combine}")
        combine.to_excel('data_sheets/carton.xlsx', index=False)

        # pizza box
        file_url = "/sites/TPDC%20Web%20Portal/PEC/MED/Shared%20Documents/MED%20Public/MED%20Carton,%20Box%20Dimension%20Search.xls"
        response = File.open_binary(ctx, file_url)
        bytes_file_obj = io.BytesIO()
        bytes_file_obj.write(response.content)
        bytes_file_obj.seek(0)
        df = pd.read_excel(bytes_file_obj, sheet_name=None, skiprows=1)
        combine = pd.Series(name="料號")
        for k in df.keys():
            if re.search("pizza box input data", k) != None:
                combine = pd.concat([combine, df[k]['料號']], axis=0, ignore_index=True)
        sp2_logger.info(f"Pizza box: {combine}")
        combine.to_excel('data_sheets/pizza box.xlsx', index=False)
        
        time.sleep(600)
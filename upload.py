import os
import re
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
for file in file_list:
    file.Delete()

file = drive.CreateFile({'title': 'Server_Address.txt'})
while True:
    ip_list = []
    ip_result = os.popen('ipconfig','r').read()
    ip_result = re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ip_result, re.I)
    for ip in ip_result:
        ip_list.append(ip.group())
    for ip in ip_list:
        if ip[:3] == "172" and ip.split('.')[3] != '1':
            file.SetContentString(f"https://{ip}:{5000}/")
            break
    file.Upload()
    time.sleep(5)
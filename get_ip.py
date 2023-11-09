'''
抓取本機IPv4地址
'''
import os, re, time, shutil, logging
def get_ipv4(PORT: int) -> None:
    '''ipv4地址寫檔至Server_Address.txt'''
    file_handler = logging.FileHandler('log.txt')
    logging.basicConfig(
        format="[%(asctime)s][%(name)-5s][%(levelname)-5s] %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    formatter = logging.Formatter(
        "[%(asctime)s][%(name)-5s][%(levelname)-5s] %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    ip_logger = logging.getLogger('main.sub_IP')
    ip_logger.setLevel(logging.DEBUG)
    ip_logger.addHandler(file_handler)
    ip_list = []
    ip_result = os.popen('ipconfig','r').read()
    ip_result = re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ip_result, re.I)
    for ip in ip_result:
        ip_list.append(ip.group())
    with open('./Server_Address.txt', 'w') as f:
        f.write(f"https://{ip_list[2]}:{PORT}/")
    ip_logger.info(f"Get IP: https://{ip_list[2]}:{PORT}/")
    return

def alive_get_ipv4(PORT: int) -> None:
    '''每1分鐘抓一次IP'''
    while True:
        get_ipv4(PORT)
        time.sleep(60)

def remove_pycache() -> None:
    '''每5分鐘刪一次cache'''
    file_handler = logging.FileHandler('log.txt')
    logging.basicConfig(
        format="[%(asctime)s][%(name)-5s][%(levelname)-5s] %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    formatter = logging.Formatter(
        "[%(asctime)s][%(name)-5s][%(levelname)-5s] %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    cache_logger = logging.getLogger('main.sub_remove_pycache')
    cache_logger.setLevel(logging.DEBUG)
    cache_logger.addHandler(file_handler)
    while True:
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")
        cache_logger.info(f"Remove __pycache__")
        
        time.sleep(300)

if __name__ == "__main__":
    alive_get_ipv4(PORT=5000)
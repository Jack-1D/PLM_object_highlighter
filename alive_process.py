from get_ip import alive_get_ipv4, remove_pycache
from get_SP_file import alive_get_SP_file
import logging
import threading

if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s][%(name)-5s][%(levelname)-5s] %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main_logger = logging.getLogger('main')
    main_logger.setLevel(logging.INFO)
    main_logger.info('Start loggin')

    get_ip_thread = threading.Thread(target=alive_get_ipv4, args=(5000,))
    remove_pycache_thread = threading.Thread(target=remove_pycache)
    get_SP_thread = threading.Thread(target=alive_get_SP_file)

    get_ip_thread.start()
    remove_pycache_thread.start()
    get_SP_thread.start()

    get_ip_thread.join()
    remove_pycache_thread.join()
    get_SP_thread.join()

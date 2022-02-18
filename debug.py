import time
import datetime
import threading
import logging

class Debug:
    def __init__(self, filename):
        self.filename = filename
        # Configuracao basica do logging
        logging.basicConfig(
            filename=self.filename,
            filemode='a+',
            level=logging.DEBUG,
            format='[%(asctime)s] [%(levelname)s] [%(threadName)-10s] %(message)s',
            datefmt='%Y-%b-%d %H:%M:%S'
        )
        
    def console(self, msg, level):
        hora_rede_local = time.strftime("%H:%M:%S", time.localtime())
        self.msg = msg
        self.level = level
        print('[{} {}] [{}] {}'.format(datetime.date.today(), hora_rede_local, level, msg)) 
        if self.level == 'CRITICAL':
            logging.critical(msg)
        if self.level == 'WARNING':
            logging.warning(msg)
        else:
            logging.info(msg)

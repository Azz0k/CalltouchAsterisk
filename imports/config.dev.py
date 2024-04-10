import platform

ATS_URL = ''
DEFAULT_PAYLOAD = {'model': '',  # model and api key are from profile 
                   'apikey': '',
                   'waitingtime': '0', 'status': 'successful'}
HOST = ''  # ip address or dns name of database server
TABLE = 'cdr'  # table name
DATABASE = 'asterisk'  #database name
LOGIN = ''
PASSWORD = ''
if platform.system() == 'Windows':
    LOG_FILE_NAME = r'c:\temp\calltouch.log'
else:
    LOG_FILE_NAME = r'/var/log/calltouch.log'
WORKER_DELAY_IN_SECONDS = 60 * 60

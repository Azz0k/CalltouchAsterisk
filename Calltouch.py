from imports.asterisk_db import Asterisk
from imports.config import *
import requests
import logging
import asyncio

db = Asterisk()


def send_calls():
    db.connect()
    calls = db.get_calls()  # '2024-04-06'
    if len(calls) == 0:
        logging.log(logging.INFO, 'Nothing to send.')
    for call in calls:
        unique_id = call[0]
        call_src = call[1]
        call_dst = '374' + call[3]
        call_date = call[4].strftime('%Y-%m-%d %H:%M:%S')
        payload = DEFAULT_PAYLOAD.copy()
        payload['callid'] = unique_id
        payload['callerid'] = call_src
        payload['phonenumber'] = call_dst
        payload['destphonenumber'] = call_dst
        payload['date'] = call_date
        payload['duration'] = call[5]
        try:
            logging.log(logging.INFO, {'src': call_src, 'dst': call_dst, 'date': call_date, 'id': unique_id})
            result = requests.get(ATS_URL,
                                  params=payload)
        except requests.exceptions.RequestException as e:
            logging.log(logging.ERROR, e)
        else:
            if result.status_code == 200:
                db.update_calls(unique_id, call_date, result.text)
                logging.log(logging.INFO, 'Sent successfully, log id: ' + result.text)
            else:
                logging.log(logging.ERROR, result.text)
    db.close()


async def worker():
    while True:
        send_calls()
        await asyncio.sleep(WORKER_DELAY_IN_SECONDS)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S', filename=LOG_FILE_NAME)
    asyncio.run(worker())

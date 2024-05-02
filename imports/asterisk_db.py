import mysql.connector
from datetime import datetime
from imports.config import *
import logging
from mysql.connector import errorcode


class Asterisk:
    def __init__(self):
        self.host = HOST
        self.table = TABLE
        self.database = DATABASE
        self.login = LOGIN
        self.password = PASSWORD
        self.db = None
        self.connected = False

    def get_calls(self, date='undefined'):
        if not self.connected:
            return []
        if date == 'undefined':
            date = datetime.now().strftime('%Y-%m-%d') + '%'
        if not date.endswith('%'):
            date = date + '%'
        cursor = self.db.cursor()
        #query = 'SELECT uniqueid, src,dst,realdst,calldate,duration,userfield FROM cdr WHERE calldate like %s  and ' \
        #        'disposition="ANSWERED" and realdst like "12%" and ' \
        #        'src like "3%" and realdst!="12910303" and userfield="";'
        query = 'SELECT uniqueid, src,dst,realdst,calldate,duration,userfield FROM cdr WHERE calldate like %s  and ' \
                'disposition="ANSWERED" and realdst like "12%" and ' \
                'src like "3%" and userfield="";'
        cursor.execute(query, (date,))
        result = [x for x in cursor.fetchall() if x[3] not in EXCLUDED_NUMBERS]
        cursor.close()
        return result

    def update_calls(self, unique_id, date, log_id):
        if not self.connected:
            return
        cursor = self.db.cursor()
        query = 'UPDATE cdr SET userfield=%s WHERE calldate like %s and uniqueid=%s'
        cursor.execute(query, (log_id, date, unique_id))
        self.db.commit()

    def connect(self):
        try:
            self.connected = False
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.login,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.log(logging.ERROR, "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.log(logging.ERROR, "Database does not exist")
            else:
                logging.log(logging.ERROR, err)
        else:
            self.connected = True

    def close(self):
        self.db.close()
        self.connected = False

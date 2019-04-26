import pymysql
import datetime

from loger import loger
from configparser import ConfigParser
from getpass import getpass 


class dbModule:

    conn = None
    errMsg = 'Nothing'
    
    def setDBConnectionInfo(self, host, user, password, db):
        
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def setDBConnectionInfo(self, filetype = 'INI', configFN = ''):

        if filetype == 'INI' and configFN != '':

            config = ConfigParser()
            config.read(configFN)
            
            self.host = config.get('ConnectionInfo', 'host')
            self.user = config.get('ConnectionInfo', 'user')
            self.password = config.get('ConnectionInfo', 'password')
            self.db = config.get('ConnectionInfo', 'database')

        elif filetype == 'INPUT':

            self.host = input("HOSTNAME: ")
            self.user = input("USER: ")
            self.password = getpass(prompt='PASSWORD: ')
            self.db = input("DATABASE: ")

# MySQL and MariaDB Module
class mysqlDBM(dbModule):

    def __init__(self, filetype, configFN = ''):
        self.setDBConnectionInfo(filetype, configFN)

    def __del__(self):
        if self.conn != None:
            self.disConnect()

    def connect(self):
        
        if self.conn == None:
            try:
                self.conn = pymysql.connect(host = self.host, user = self.user, password = self.password, db = self.db)
            except Exception as e:
                self.conn = None
                self.errMsg = str(e)

    def disConnect(self):
        
        if self.conn != None:
            try:
                self.conn.close()
                self.conn = None
            except Exception as e:
                self.errMsg = str(e)

    def getScalar(self, query, params = None):
        
        rtn = None

        try:
            if self.conn == None:
                self.connect()

            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            rtn = rows[0][0]

        except Exception as e:
            self.errMsg = str(e)
        
        finally:
            cursor.close()

        return rtn

    def getResults(self, query, params = None):

        rtn = None

        try:
            if self.conn == None:
                self.connect()
                
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rtn = cursor.fetchall()
            
        except Exception as e:
            self.errMsg = str(e)

        finally:
            cursor.close()

        return rtn

    def executeNonQuery(self, query, params = None):

        rtn = None

        try:
            if self.conn == None:
                self.connect()

            cursor = self.conn.cursor()
            rtn = cursor.execute(query, params)
            self.conn.commit()
            
        except Exception as e:
            self.errMsg = str(e)

        finally:
            cursor.close()

        return rtn
    


dbo = mysqlDBM('INI', 'C:\\log\\dbinfo.ini')
print(dbo.errMsg)
cnt = dbo.getScalar('SELECT COUNT(1) FROM USERINFO')
print(cnt)
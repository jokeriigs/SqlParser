import pymysql
import datetime

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

    def __init__(self, filetype = 'INI', configFN = 'C:\\log\\dbinfo.ini'):
        self.setDBConnectionInfo(filetype, configFN)

    def __del__(self):
        if self.conn != None:
            self.disConnect()

    def connect(self, cursorclass = None):
        
        if self.conn == None:
            try:
                if cursorclass == None:
                    self.conn = pymysql.connect(host = self.host, user = self.user, password = self.password, db = self.db)
                else:
                    self.conn = pymysql.connect(host = self.host, user = self.user, password = self.password, db = self.db, cursorclass = cursorclass)
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


        return rtn

    def getResultToJson(self, query, params = None, titleList = None):

        # 여기서 부터 만들어야 함
        rtn = []

        try:

            if self.conn != None:
                self.conn.close()


            if titleList == None:
                self.connect(cursorclass=pymysql.cursors.DictCursor)
            else:
                self.connect()
                
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            if titleList != None:
                colCnt = len(rows[0])
                for row in rows:
                    rowContent = {}
                    for i in range(0, colCnt):
                        rowContent[titleList[i]] = row[i]
                    rtn.append(rowContent)
            else:
                rtn = rows
            
        except Exception as e:
            self.errMsg = str(e)

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


        return rtn

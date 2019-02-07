import pymysql
import datetime

def getSEQ(reqDT = ''):

    rtn = ''
    sql = ''
    conn = getDBConn()

    try:
        if reqDT == '':
            reqDT = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with conn.cursor() as curs:
                sql = 'INSERT INTO SQLINS_SEQ(REQDT) VALUES(%s)'
                curs.execute(sql, reqDT)
                conn.commit()
        with conn.cursor() as curs:
            sql = 'SELECT OID FROM SQLINS_SEQ WHERE REQDT = %s'
            curs.execute(sql, reqDT)

            rows = curs.fetchall()
            
            for row in rows:
                rtn = row[0]

    except Exception as e:
        print(e)
    finally:
        conn.close()

    return rtn

def getDBConn():
    
    conn = pymysql.connect( host='localhost', \
                                  user='root', \
                                  password='Qwerasdf11@@', \
                                  db='mysql')

    return conn

pkey = getSEQ()

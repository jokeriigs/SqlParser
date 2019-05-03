from okUtil import dbModule

dbo = dbModule.mysqlDBM('INI', 'C:\\log\\dbinfo.ini')

jsonData = dbo.getResultToJson('select	oid, author, title, contents, date_posted from	posts')
print (jsonData)

# import pymysql

# conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'Qwerasdf11@@', db = 'pms')

# curs = conn.cursor()
# curs.execute("select	oid, author, title, contents, date_posted from		posts")

# results = curs.fetchall()

# print(results)

# conn.close()

# # for i in range(0, 10):
# #     print (i)
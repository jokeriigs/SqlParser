import sys

sys.path.append('C:\\Users\\okung_kwon\\Documents\\Python Projects')

from okUtil import dbModule, security, loger
from datetime import datetime

import socket

class MemberMgmt:

    def register(self, request):

        msg = ''

        userId = request.form['userid']
        password = security.HashSHA256(request.form['password'])
        userName = request.form['username']
        eMail = request.form['userEmail']
        phoneNumber = request.form['phoneNumber']
        company = request.form['company']
        companyPart = request.form['companyPart']

        regDatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        regIp = socket.gethostbyname(socket.getfqdn())

        dbo = dbModule.mysqlDBM()
        query = "SELECT COUNT(1) FROM USERINFO WHERE USERID = %s"
        userCnt = dbo.getScalar(query, (userId))

        if userCnt == 0:
            query = """
                INSERT INTO USERINFO(
                                        USERID
                                        , PASSWORD
                                        , USERNAME
                                        , EMAIL
                                        , PHONENUMBER
                                        , COMPANY
                                        , COMPANYPART
                                        , REGDT
                                        , REGIP
                                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            msg = dbo.executeNonQuery(query, (userId, password, userName, eMail, phoneNumber, company, companyPart, regDatetime, regIp))

            if msg == None:
                msg = dbo.errMsg
            else:
                msg = 'SUCC'
        else:
            msg = '중복 아이디가 존재합니다.'

        return msg

    def login(self, request, session):

        msg = ''
        userId = request.form['userid']
        password = security.HashSHA256(request.form['password'])

        dbo = dbModule.mysqlDBM()
        rst = dbo.getResults("SELECT COUNT(1), USERNAME FROM USERINFO WHERE USERID = %s AND PASSWORD = %s", (userId, password))

        if rst == None:
            msg = dbo.errMsg
        elif rst[0][0] == 1:
            msg = 'SUCC'
            session['userid'] = userId
            session['userName'] = rst[0][1]
        else:
            msg = 'ID 또는 비밀번호가 상이합니다.'

        return msg

    def getUserList(self, request):

        rtn = ''
        
        try:
            searchVal = request.form['searchval']
        except:
            searchVal = ''

        searchVal = "%" + searchVal + "%"

        dbo = dbModule.mysqlDBM()
        rst = dbo.getResults("SELECT USERID, USERNAME FROM USERINFO WHERE USERID LIKE %s OR USERNAME LIKE %s", (searchVal, searchVal))

        for item in rst:
            rtn += item[0] + '@' + item[1] + '@@'


        return rtn

    def sendMessage(self, request, session):

        rtn = 'SUCC'

        dt = datetime.now()
        msgKey = dt.strftime('%Y%m%d%H%M%S') + str(dt.microsecond) + session['userid']
        author = session['userid']
        receiver = request.form['receivers']
        cc = request.form['cc']
        hiddencc = request.form['hiddencc']
        title = request.form['title']
        contents = request.form['contents']
        # attached = request.form['attached']
        regdate = dt.strftime('%Y-%m-%d %H:%M:%S')
        regip = socket.gethostbyname(socket.getfqdn())
        dbo = dbModule.mysqlDBM()

        try:
            query = """
                INSERT INTO MESSAGEMAIN(
                    MSGKEY
                    , AUTHOR
                    , RECEIVER
                    , CC
                    , HIDDENCC
                    , TITLE
                    , CONTENTS
                    , REGDATE
                    , REGIP
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            dbo.executeNonQuery(query, (msgKey, author, receiver, cc, hiddencc, title, contents, regdate, regip))

            query = """
                INSERT INTO MESSAGEDETAIL(
                    MSGKEY
                    , RECVUSERID
                    , RECVTYPE
                    , REGDT
                    , REGIP
                ) VALUES (%s, %s, %s, %s, %s)
            """

            for item in receiver.split(';'):
                if item != '':
                    startpos = item.find('[')
                    endpos = item.find(']')

                    dbo.executeNonQuery(query, (msgKey, item[startpos+1:endpos], 'R', regdate, regip))

            for item in cc.split(';'):
                if item != '':
                    startpos = item.find('[')
                    endpos = item.find(']')

                    dbo.executeNonQuery(query, (msgKey, item[startpos+1:endpos], 'C', regdate, regip))

            for item in hiddencc.split(';'):
                if item != '':
                    startpos = item.find('[')
                    endpos = item.find(']')

                    dbo.executeNonQuery(query, (msgKey, item[startpos+1:endpos], 'H', regdate, regip))
        except:
            rtn = dbo.errMsg
            loger.loger.logging(rtn)

        return rtn

    
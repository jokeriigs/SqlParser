import os
import sys
sys.path.append('C:\\Users\\okung_kwon\\Documents\\Python Projects')

from flask import Flask, session, redirect, url_for, escape, request, render_template
from okUtil import dbModule, security, loger
from datetime import datetime
from bizLogic import pmsmgmt

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/404')
def notFound():
    return render_template('404.html')

@app.route('/blank')
def blank():
    return render_template('blank.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/forms')
def forms():
    return render_template('forms.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/inbox')
def inbox():
    return render_template('inbox.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ''

    if request.method == 'POST':
        objBiz = pmsmgmt.MemberMgmt()
        msg = objBiz.login(request, session)
        if msg == 'SUCC':
            return redirect('/')
    
    return render_template('signin.html', htmlMsg = msg)

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    msg = ''
    
    if request.method == 'POST':
        objBiz = pmsmgmt.MemberMgmt()
        msg = objBiz.register(request)

        if msg == 'SUCC':
            return redirect('/login')
            
    return render_template('signup.html', htmlMsg = msg)

@app.route('/typography')
def typography():
    return render_template('typography.html')

@app.route('/validation')
def validation():
    return render_template('validation.html')

@app.route('/compose', methods=['GET', 'POST'])
def compose():
    if request.method == 'POST':
        objBiz = pmsmgmt.MemberMgmt()
        msg = objBiz.sendMessage(request, session)
        return msg
    else:
        return render_template('compose.html')

@app.route('/userSearch', methods=['GET', 'POST'])
def userSearch():
    objBiz = pmsmgmt.MemberMgmt()
    msg = objBiz.getUserList(request)
    return msg

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():

#     contents = ''

#     if request.method == 'POST':
#         userid = request.form['userid']
#         password = security.HashSHA256(request.form['password'])
#         rows = dbo.getResults('SELECT PASSWORD FROM USERINFO WHERE USERID = %s', (userid))

#         if rows == None or len(rows) == 0:
#             contents = '<script>alert("해당 아이디가 존재하지 않습니다.")</script>'
#         elif password != rows[0][0]:
#             contents = '<script>alert("비밀번호가 상이합니다.")</script>'
#         else:
#             contents = '<script>alert("로그인에 성공하였습니다.")</script>'
#             session['userid'] = userid
#         # return redirect(url_for('index'))
#     contents += '''
#         <form action="" method="post">
#             <p>유저아이디: <input type=text name=userid id=userid>
#             <p>비밀번호: <input type=password name=password id=password>
#             <p><input type=submit value=Login>
#         </form>'''

#     return contents

# @app.route('/register', methods=['GET', 'POST'])
# def register():
    
#     rtn = ''
    
#     if request.method == 'POST':

#         msg = ''
#         username = request.form['username']
#         userid = request.form['userid']
#         password = request.form['password']

#         userCnt = dbo.getScalar('SELECT COUNT(1) FROM USERINFO WHERE USERID = %s', (userid))

#         if userCnt != 0:
#             msg = '중복된 아이디가 존재합니다.'
#         else:
#             dbo.executeNonQuery('INSERT INTO USERINFO(USERID, PASSWORD, USERNAME) VALUES (%s,%s,%s)', (userid, security.HashSHA256(password), username))

#         if msg == 'SUCC':
#             msg = '등록 성공'

#         rtn = "<script>alert('" + msg + "')</script>"
        
#     rtn += '''
    
#     <form action="" method="post">
#         사용자명 : <input type="text" name="username" id="username"/><br/>
#         id : <input type="text" name="userid" id="userid"/><br/>
#         password : <input type='password' name='password' id='password'/><br/>
#         <input type=submit value='register'>
#     </form>
#     '''

#     return rtn

if __name__ == '__main__':
    app.secret_key = 'developer'
    app.run(debug=True)